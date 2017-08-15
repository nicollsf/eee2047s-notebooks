from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
@magics_class
class MyMagics(Magics):

    @line_magic
    def setupsave(self, line):
        """Generate filename variables for saving cells"""
        for i in range(1, 9):
            cpystr = 'nbpy'+str(i)+'name="../src/'+line+'-'+str(i)+'.py"'
            self.shell.run_cell(cpystr)
    
    @cell_magic
    def writefileexec(self, line, cell):
        """Modified writefile with subsequent cell execution"""
        
        # process magic command line
        args = line.split('#',1)[0]  # strip trailing comment
        argl = args.split(' ')
        argl = [t for t in argl if t!='']
        argln = [t for t in argl if t[0]!='-']
        if len(argln)!=1:  raise Exception('No filename specified')
        argls = [t for t in argl if t=='-s']
        
        # save as required
        lcell = cell.split('\n')
        si = 0
        while lcell[si]=='':  si = si + 1
        f = open(argln[0], 'w')
        for ci in range(si, len(lcell)):
            cl = lcell[ci]
            if len(argls)>0 and len(cl)>0 and cl[0]=='%':  continue
            f.write(cl + '\n')  # write line
        f.close()
        
        # execute
        self.shell.run_cell(cell)  # run cell

ip = get_ipython()
ip.register_magics(MyMagics)
