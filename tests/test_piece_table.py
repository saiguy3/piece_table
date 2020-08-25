from piece_table import PieceTable
import unittest


class TestPieceTable(unittest.TestCase):
    def setUp(self):
        self.long_string = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent maximus"
            " fringilla porta. Nulla at est in magna faucibus dictum. Suspendisse varius"
            " diam in nunc blandit, sed posuere orci pharetra. Maecenas hendrerit odio non"
            " accumsan euismod. Sed ullamcorper, arcu non ullamcorper sodales, ex diam"
            " pretium magna, sed fermentum purus mauris laoreet ex. Etiam neque diam,"
            " posuere quis sodales sed, ultricies quis leo. Fusce metus justo, ornare a"
            " vestibulum ac, lacinia at tellus. Ut pulvinar convallis nulla ut congue."
            " Aliquam est leo, consequat a arcu eu, consequat consectetur libero. Nunc"
            " mattis mollis purus, a scelerisque orci commodo volutpat. Mauris tempor lorem"
            " nec ipsum ornare sodales."
        )
        self.short_string = "[Text]"

    def test_length(self):
        piece_table = PieceTable(self.long_string)
        self.assertEqual(len(self.long_string), len(piece_table))

    def test_integer_index(self):
        piece_table = PieceTable(self.long_string)
        self.assertEqual(self.long_string[1], piece_table[1])

    def test_splice_index(self):
        piece_table = PieceTable(self.long_string)
        self.assertEqual(self.long_string[10:12], piece_table[10:12])
        self.assertEqual(self.long_string[-5:], piece_table[-5:])
        self.assertEqual(self.long_string[:-5], piece_table[:-5])

    def test_get_piece_and_offset(self):
        piece_table = PieceTable(self.long_string)
        piece_index, piece_offset = piece_table.get_piece_and_offset(1)
        self.assertEqual(piece_index, 0)
        self.assertEqual(piece_offset, 1)

    def test_get_piece_and_offset_lower_index_erro(self):
        piece_table = PieceTable(self.long_string)
        self.assertRaises(IndexError, piece_table.get_piece_and_offset, -1)

    def test_get_piece_and_offset_upper_index_error(self):
        piece_table = PieceTable(self.long_string)
        self.assertRaises(
            IndexError, piece_table.get_piece_and_offset, len(self.long_string) + 1
        )

    def test_insert_start(self):
        piece_table = PieceTable(self.long_string)
        piece_table.insert(self.short_string, 0)
        ret = piece_table.get_text()
        expected = self.short_string + self.long_string
        self.assertEqual(ret, expected)

    def test_insert_middle(self):
        piece_table = PieceTable(self.long_string)
        piece_table.insert(self.short_string, 10)
        ret = piece_table.get_text()
        expected = self.long_string[:10] + self.short_string + self.long_string[10:]
        self.assertEqual(ret, expected)

    def test_insert_end(self):
        piece_table = PieceTable(self.long_string)
        piece_table.insert(self.short_string, len(self.long_string))
        ret = piece_table.get_text()
        expected = self.long_string + self.short_string
        self.assertEqual(ret, expected)

    def test_delete_start(self):
        piece_table = PieceTable(self.long_string)
        piece_table.delete(0, 10)
        ret = piece_table.get_text()
        expected = self.long_string[10:]
        self.assertEqual(ret, expected)

    def test_delete_middle(self):
        piece_table = PieceTable(self.long_string)
        piece_table.delete(10, 10)
        ret = piece_table.get_text()
        expected = self.long_string[:10] + self.long_string[20:]
        self.assertEqual(ret, expected)

    def test_delete_end_negative_length(self):
        piece_table = PieceTable(self.long_string)
        piece_table.delete(len(self.long_string), -10)
        ret = piece_table.get_text()
        expected = self.long_string[:-10]
        self.assertEqual(ret, expected)

    def test_delete_lower_index_error(self):
        piece_table = PieceTable(self.long_string)
        self.assertRaises(IndexError, piece_table.delete, -1, 10)

    def test_delete_upper_index_error(self):
        piece_table = PieceTable(self.long_string)
        self.assertRaises(IndexError, piece_table.delete, len(self.long_string) + 1, 10)

    def test_string_at(self):
        piece_table = PieceTable(self.long_string)
        piece_table.insert(self.short_string, 10)
        ret = piece_table.string_at(10, len(self.short_string))
        self.assertEqual(ret, self.short_string)


if __name__ == "__main__":
    unittest.main()
