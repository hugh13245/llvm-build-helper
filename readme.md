# llvm-build-helper

The current repository contains a python script 'build.py' and a configuration file 'config.json' to simplify the acquisition and compilation of llvm/clang/extra source code.  

## config.json

```json
{
    "llvm":{
        "url":"https://github.com/llvm-mirror/llvm.git",
        "branch":"release_80",
        "version":""
    },
    "clang":{
        "url":"https://github.com/llvm-mirror/clang.git",
        "branch":"release_80"
    },
    "extra":{
        "url":"ssh://git@gitlab.foxitsoftware.cn:234/foxit/clang-tools-extra.git",
        "branch":"base_llvm_clang_8.0"
    },
	"generate":{
	    "dir":"build"
	},
    "build":{   
        "target":"clang-tidy",
        "version":"Release"
    }
}
```

You can do what you want by adding changes to the default configuration, and of course you can expand these configurations.

# build.py

```
usage: build.py [-h] [-update] [-build] [-generate]
                [-config Configuration files] [-target TARGET]
                [-version VERSION]

Clone,update,build llvm/clang/extra with specified configuration

optional arguments:
  -h, --help            show this help message and exit
  -update               Update repository
  -build                Build repository
  -generate             Generate project
  -config Configuration files
                        Configuration files
  -target TARGET        Build target. Works only when the 'build' option
                        exists,you can override the 'build/target' options
                        specified in the configuration file
  -version VERSION      Build version. Works only when the 'build' option
                        exists,you can override the 'build/version' options
                        specified in the configuration file
```

# example

Make sure that cmake, python 3.x have installed on your machine.

```
python build.py -update -generate -build
```

