#!/usr/bin/env python
import sys
from pdfrw import PdfReader, PdfWriter

class PDFOperator(object):
	@classmethod
	def name():
		raise (NotImplemented)

	@classmethod
	def hint():
		raise (NotImplemented)


class PDFInsert(PDFOperator):
	@classmethod
	def name(cls):
		return '-i'

	@classmethod
	def hint(cls):
		return '  {} <A> <B> <PN> [<Dest>]:\n    Inserts B into A after page PN and writes the new file to Dest. The default destination is A'.format(cls.name())

	def __init__(self, a, b, pn_str, dest=None):
		pn = int(pn_str)

		readerA = PdfReader(a)
		if pn < 0 or pn > len(readerA.pages):
			raise Exception('PN needs to be between 0 and {} for file {}'.format(len(readerA.pages), a))

		readerB = PdfReader(b)

		newPages = readerA.pages[:pn] + readerB.pages + readerA.pages[pn:]
		if dest == None:
			dest = a

		PdfWriter().addpages(newPages).write(dest)


class PDFAppendNew(PDFOperator):
	@classmethod
	def name(cls):
		return '-an'

	@classmethod
	def hint(cls):
		return '  {} <Dest> <F1> <F2> [<F3> ....]:\n    Appends the given files and writes the new pdf to Dest.'.format(cls.name())

	def __init__(self, dest, *args):
		if len(args) < 2:
			raise Exception('Need at least 2 files to append to each other.')

		writer = PdfWriter()

		for fname in args:
			writer.addpages(PdfReader(fname).pages)

		writer.write(dest)

class PDFAppend(PDFOperator):
	@classmethod
	def name(cls):
		return '-a'

	@classmethod
	def hint(cls):
		return '  {} <F1> <F2> [<F3> ....]:\n    Appends the given files to F1.'.format(cls.name())

	def __init__(self, *args):
		if len(args) < 2:
			raise Exception('Need at least 2 files to append to each other.')

		PDFAppendNew(args[0], *args)


if __name__ == '__main__':
	ops = {op.name(): op for op in [PDFInsert, PDFAppendNew, PDFAppend]}

	args = sys.argv

	if '-h' in args or len(args) < 2:
		for op in ops.values():
			print(op.hint())
	else:
		try:
			op = ops[args[1]]
			try:
				op(*args[2:])
			except Exception as e:
				print(e) 
		except:
			print('Unknown operation {}. Use -h for help.'.format(args[1]))
