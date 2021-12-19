#!/usr/bin/env python
import sys
from pdfrw import PdfReader, PdfWriter

def get_document_pages(file_arg):
    args = file_arg.split('[')
    if len(args) == 1:
        return PdfReader(args[0]).pages
    else:
        fn = args[0]
        if args[1][-1] != ']':
            raise Exception('Parse error in "{}": Missing closing ]'.format(file_arg))

        document = PdfReader(fn)
        ranges   = args[1][:-1].split(',')
        pnumbers = range(len(document.pages))
        spages   = set()
        for r in ranges:
            if ':' in r:
                b, e = r.split(':')
                if b != '' and e != '':
                    b = int(b) - 1 if int(b) > 0 else int(b)
                    spages = spages.union(set(pnumbers[b:int(e)]))
                elif e != '':
                    spages = spages.union(set(pnumbers[:int(e)]))
                elif b != '':
                    b = int(b) - 1 if int(b) > 0 else int(b)
                    spages = spages.union(set(pnumbers[b:]))
                else:
                    spages = set(pnumbers)
            else:
                p = int(r)
                if p > 0:
                    p -= 1
                elif p == 0:
                    raise Exception('Page number 0 given in {} is invalid.'.format(file_arg))
                
                if abs(p) > pnumbers[-1]:
                    raise Exception('Wrong page number given in "{}". "{}" has only {} pages.'.format(file_arg, fn, len(pnumbers)))
                spages.add(pnumbers[p])

        return [document.pages[p] for p in sorted(spages)]


class PDFOperator(object):
    @classmethod
    def name():
        raise NotImplementedError

    @classmethod
    def hint():
        raise NotImplementedError


class PDFInsert(PDFOperator):
    @classmethod
    def name(cls):
        return '-i'

    @classmethod
    def hint(cls):
        return '  {} <A> <B[]> <PN> [<Dest>]:\n    Inserts B into A after page PN and writes the new file to Dest. The default destination is A'.format(cls.name())

    def __init__(self, a, b, pn_str, dest=None):
        pn = int(pn_str)

        readerA = PdfReader(a)
        if pn < 0 or pn > len(readerA.pages):
            raise Exception('PN needs to be between 0 and {} for file {}'.format(len(readerA.pages), a))

        newPages = readerA.pages[:pn] + get_document_pages(b) + readerA.pages[pn:]
        if dest is None:
            dest = a

        PdfWriter().addpages(newPages).write(dest)


class PDFAppendNew(PDFOperator):
    @classmethod
    def name(cls):
        return '-an'

    @classmethod
    def hint(cls):
        return '  {} <Dest> <F1[]> <F2[]> [<F3[]> ....]:\n    Appends the given files and writes the new pdf to Dest.'.format(cls.name())

    def __init__(self, dest, *args):
        if len(args) < 2:
            raise Exception('Need at least 2 files to append to each other.')

        writer = PdfWriter()

        for fname in args:
            writer.addpages(get_document_pages(fname))

        writer.write(dest)

class PDFAppend(PDFOperator):
    @classmethod
    def name(cls):
        return '-a'

    @classmethod
    def hint(cls):
        return '  {} <F1> <F2[]> [<F3[]> ....]:\n    Appends the given files to F1.'.format(cls.name())

    def __init__(self, *args):
        if len(args) < 2:
            raise Exception('Need at least 2 files to append to each other.')

        PDFAppendNew(args[0], *args)


class PDFSlice(PDFOperator):
    @classmethod
    def name(cls):
        return '-s'

    @classmethod
    def hint(cls):
        return '  {} <File[]> [<Dest>]:\n    Slices the given file as specified by the range operator and saves it. Pass Dest to create a new file.'.format(cls.name())

    def __init__(self, *args):
        if len(args) < 1:
            raise Exception('Need at least a file to slice.')

        dest = args[0].split('[')[0] if len(args) == 1 else args[1]
        PdfWriter().addpages(get_document_pages(args[0])).write(dest)


class PDFInverse(PDFOperator):
    @classmethod
    def name(cls):
        return '-r'

    @classmethod
    def hint(cls):
        return '  {} <File[]> [<Dest>]:\n    Reverses and slices the given file. Pass Dest to create new file.'.format(cls.name())

    def __init__(self, *args):
        if len(args) < 1:
            raise Exception('Need at least a file to slice.')

        dest = args[0].split('[')[0] if len(args) == 1 else args[1]
        PdfWriter().addpages(reversed(get_document_pages(args[0]))).write(dest)


class PDFMerge(PDFOperator):
    @classmethod
    def name(cls):
        return '-m'

    @classmethod
    def hint(cls):
        return '  {} <Dest> <F1[]> <F2[]> [<F3[]> ....]:\n    Merges the given files into Dest, by appending their pages sequentially.'.format(cls.name())    

    def __init__(self, *args):
        if len(args) < 3:
            raise Exception('Need at least three arguments.')

        pages  = [get_document_pages(d) for d in args[1:]]
        writer = PdfWriter()
        eof = False
        while not eof:
            eof = True
            for x in range(len(pages)):
                if len(pages[x]) > 0:
                    writer.addpages(pages[x][:1])
                    pages[x] = pages[x][1:]
                    eof = False
        writer.write(args[0])


class PDFPagify(PDFOperator):
    @classmethod
    def name(cls):
        return '-p'

    @classmethod
    def hint(cls):
        return '  {} <File[]> [<Dest>]:\n    Splits given file into one file per page. Pass Dest to give prefix for resulting files.'.format(cls.name())

    def __init__(self, *args):
        if len(args) < 1:
            raise Exception('Need one file to split.')

        dest = args[0][:-4] if len(args) == 1 else args[1]
        for x, page in enumerate(get_document_pages(args[0])):
            PdfWriter().addpages([page]).write(f'{dest}{x}.pdf')


if __name__ == '__main__':
    ops = {op.name(): op for op in [PDFSlice, PDFInsert, PDFAppendNew, PDFAppend, PDFInverse, PDFMerge, PDFPagify]}

    args = sys.argv

    if '-h' in args or len(args) < 2:
        for op in ops.values():
            print(op.hint())
        print('\nParameters with a "[]" at the end support range selection of pages.\nUse "my.pdf[1]" to get only the first page of "my.pdf", or "my.pdf[:5]"\nto get the first five pages.\nYou can also combine ranges and indices, eg. "my.pdf[1,3,4:9,-1]" selects\nthe first, third and last page of the document, as well as all pages 4, 5, 6, 7, 8 and 9.')
    else:
        try:
            op = ops[args[1]]
            try:
                op(*args[2:])
            except Exception as e:
                print(e) 
        except KeyError:
            print('Unknown operation {}. Use -h for help.'.format(args[1]))
