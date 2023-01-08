import ast, re, pathlib, shutil, pathlib
import numpy as np
import argparse


# Ф-ция удаляющая комментарии
def remove_comments(source):
    string = re.sub(re.compile("'''.*?'''", re.DOTALL), "", source)
    string = re.sub(re.compile('""".*?"""', re.DOTALL), "", source)
    return string


# Ф-ция которая принимает пути до файлов, делает их текстовыми и строит абстрактное синт. дерево
def make_clean_ast(pyfile_path1, pyfile_path2):
    signs = [']', '[', '(', ')', ',', "'"]

    nwn1 = pyfile_path1[:-3] + 'copy1' + '.py'
    nwn2 = pyfile_path2[:-3] + 'copy2' + '.py'

    shutil.copyfile(pyfile_path1, nwn1)
    shutil.copyfile(pyfile_path2, nwn2)

    nwn1 = pathlib.Path(nwn1)
    nwn2 = pathlib.Path(nwn2)

    nwp = str([part + '/' for part in list(str(nwn1).split('/')[:-1])]).replace(']', '').replace('[',
                                                                                                 '').replace(
        ',', '').replace("'", '').replace(' ', '')
    nwn1.rename(nwp + 'copy1' + '.txt')
    copy1 = nwp + 'copy1' + '.txt'
    nwp = str([part + '/' for part in list(str(nwn2).split('/')[:-1])]).replace(']', '').replace('[',
                                                                                                 '').replace(
        ',', '').replace("'", '').replace(' ', '')
    nwn2.rename(nwp + 'copy2' + '.txt')
    copy2 = nwp + 'copy2' + '.txt'

    f = open(copy1)
    n1 = ""
    for _ in f:
        n1 += _
    n1 = remove_comments(n1)
    tree1 = ast.parse(source=n1)
    ast_code1 = ast.dump(tree1, annotate_fields=False)
    for g in signs:
        ast_code1 = ast_code1.replace(g, ' ')
    ast_code1 = re.sub(" +", " ", ast_code1)

    f = open(copy2)
    n2 = ""
    for _ in f:
        n2 += _
    n2 = remove_comments(n2)
    tree2 = ast.parse(source=n2)
    ast_code2 = ast.dump(tree2, annotate_fields=False)
    for g in signs:
        ast_code2 = ast_code2.replace(g, ' ')
    ast_code2 = re.sub(" +", " ", ast_code2)

    return ast_code1, ast_code2


# Ф-ция считает расстояние Левенштейна по буквам
def levenstein(s1, s2):
    lev = np.zeros((len(s1), len(s2)))
    for i in range(len(s1)):
        for j in range(len(s2)):
            if min(i, j) == 0:
                lev[i, j] = max(i, j)
            else:
                x, y, z = lev[i - 1, j], lev[i, j - 1], lev[i - 1, j - 1]
                lev[i, j] = min([x, y, z])
                if s1[i] != s2[j]:
                    lev[i, j] += 1
    res = 1 - (lev[-1, -1]) / (max(len(s1), len(s2)))
    return res


# Консольный ввод
parser = argparse.ArgumentParser()
parser.add_argument('indir', type=str)
parser.add_argument('outdir', type=str)
args = parser.parse_args()
inp = args.indir
outp = args.outdir
source = open(inp, 'r')
result = open(outp, 'w')

for _ in source:
    path1, path2 = list(map(str, _.split()))
    code_ast1, code_ast2 = make_clean_ast(path1, path2)
    result.write(str(levenstein(code_ast1, code_ast2)) + '\n')
