from cx_Freeze import setup, Executable

buildOptions = dict(include_files = [('C:\Users\Radu\workspace\Femo\save','save')])

setup(name = "Femo" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("Femo.py")],
      options = dict(build_exe = buildOptions)
    )