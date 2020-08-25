class _Piece:
    """
    Struct to contain metadata for a piece.

    Attributes:
        in_added (bool): whether to look at the add buffer or the orignal
        offset (int): start of the piece in appropriate buffer
        length (int): length of the piece in appropriate buffer
    """

    def __init__(self, in_added, offset, length):
        self.in_added = in_added
        self.offset = offset
        self.length = length


class PieceTable:
    """
    Implementation of a piece table.

    Attributes:
        document (string): original contents to start the piece table
    """

    def __init__(self, document):
        self._text_len = len(document)
        self._original = document
        self._added = ""
        self.pieces = [_Piece(False, 0, len(document))]

    def __len__(self):
        """
        Get length of text sequence in the piece table.
        """
        return self._text_len

    def __getitem__(self, key):
        """
        Allow integer indexing and slicing into the text sequence in the piece table.
        """
        if isinstance(key, int):
            return self.string_at(key, 1)
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return self.string_at(start, stop - start)[::step]
        else:
            raise TypeError("Index must be int, not {}".format(type(key).__name__))

    def replace_pieces(self, start, replace_count, items):
        """
        Add/replace piece(s) in the pieces array.

        Parameters:
            start (int): starting index of where to add items
            replace_count (int): number of items to replaces
            items (list[_Piece]): list of new pieces

        Returns:
            list[_Piece]: pieces array after the edits
        """
        return self.pieces[:start] + items + self.pieces[start + replace_count:]

    def get_piece_and_offset(self, index):
        """
        Find corresponding piece that contains the character at the index.

        Parameters:
            offset (int): index into the text

        Returns:
            tuple(int, int): tuple of the piece table index and offset into that piece's buffer
        """
        if index < 0:
            raise IndexError("Text index cannot be below 0")

        remainingOffset = index
        for i in range(len(self.pieces)):
            piece = self.pieces[i]
            if remainingOffset <= piece.length:
                return (i, piece.offset + remainingOffset)
            remainingOffset -= piece.length

        raise IndexError("Text index cannot be greater than the length of the text")

    def insert(self, text, index):
        """
        Insert a string into the piece table.

        Parameters:
            text (string): the string to insert
            index (int): the index at which to insert the string
        """
        if len(text) == 0:
            return

        # Get piece to insert into
        piece_index, piece_offset = self.get_piece_and_offset(index)
        curr_piece = self.pieces[piece_index]

        # Append text to added buffer
        added_offset = len(self._added)
        self._added += text
        self._text_len += len(text)

        # If insertion is at the end and the piece points to the end of the add buffer,
        # just increase the length
        if (
            curr_piece.in_added
            and piece_offset == curr_piece.offset + curr_piece.length == added_offset
        ):
            curr_piece.length += len(text)
            return

        # Split current piece into three separate pieces
        insert_pieces = [
            _Piece(
                curr_piece.in_added, curr_piece.offset, piece_offset - curr_piece.offset
            ),
            _Piece(True, added_offset, len(text)),
            _Piece(
                curr_piece.in_added,
                piece_offset,
                curr_piece.length - (piece_offset - curr_piece.offset),
            ),
        ]
        insert_pieces = list(filter(lambda piece: piece.length > 0, insert_pieces))

        self.pieces = self.replace_pieces(piece_index, 1, insert_pieces)

    def delete(self, index, length):
        """
        Delete a string from the piece table.

        Parameters:
            index (int): the index at which to start deletion
            length (int): the number of characters to delete (if negative, deletes backwards)
        """
        if length == 0:
            return
        if length < 0:
            self.delete(index + length, -length)
            return
        if index < 0:
            raise IndexError("Text index out of range")

        # Get affected pieces (may span multiple pieces)
        start_piece_index, start_piece_offset = self.get_piece_and_offset(index)
        stop_piece_index, stop_piece_offset = self.get_piece_and_offset(index + length)
        self._text_len -= length

        # If single piece, check if delete is at the start or end the piece
        if start_piece_index == stop_piece_index:
            piece = self.pieces[start_piece_index]

            if start_piece_offset == piece.offset:
                piece.offset += length
                piece.length -= length
                return
            elif stop_piece_offset == piece.offset + piece.length:
                piece.length -= length
                return

        start_piece = self.pieces[start_piece_index]
        end_piece = self.pieces[stop_piece_index]

        # Split existing pieces into two separate pieces
        delete_pieces = [
            _Piece(
                start_piece.in_added,
                start_piece.offset,
                start_piece_offset - start_piece.offset,
            ),
            _Piece(
                end_piece.in_added,
                stop_piece_offset,
                end_piece.length - (stop_piece_offset - end_piece.offset),
            ),
        ]
        delete_pieces = list(filter(lambda piece: piece.length > 0, delete_pieces))

        delete_count = stop_piece_index - start_piece_index + 1
        self.pieces = self.replace_pieces(
            start_piece_index, delete_count, delete_pieces
        )

    def get_text(self):
        """
        Gets the text sequence of the piece table as a string.

        Returns:
            string: text sequence
        """
        document = ""
        for piece in self.pieces:
            if piece.in_added:
                document += self._added[piece.offset:piece.offset + piece.length]
            else:
                document += self._original[piece.offset:piece.offset + piece.length]
        return document

    def string_at(self, index, length):
        """
        Gets a string of a particular length from the text sequence as a string.

        Parameters:
            index (int): the index at which to start lookup
            length (int): the number of characters to lookup (if negative, looks backwards)

        Returns:
            string: text sequence
        """
        if length < 0:
            return self.string_at(index + length, -length)

        document = ""

        # Get affected pieces (may span multiple pieces)
        start_piece_index, start_piece_offset = self.get_piece_and_offset(index)
        stop_piece_index, stop_piece_offset = self.get_piece_and_offset(index + length)

        start_piece = self.pieces[start_piece_index]
        buffer = self._added if start_piece.in_added else self._original

        # If single piece, return text from piece
        if start_piece_index == stop_piece_index:
            document = buffer[start_piece_offset:start_piece_offset + length]
        else:
            document = buffer[start_piece_offset:start_piece.offset + start_piece.length]
            for i in range(start_piece_index + 1, stop_piece_index + 1):
                cur_piece = self.pieces[i]
                buffer = self._added if cur_piece.in_added else self._original

                # If the ending piece, only add remaining length to the string
                if i == stop_piece_index:
                    document += buffer[cur_piece.offset:stop_piece_offset]
                else:
                    document += buffer[cur_piece.offset:cur_piece.offset + cur_piece.length]

        return document
