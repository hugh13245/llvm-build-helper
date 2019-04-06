import json
import os
import sys
import argparse

def update_repo(dir,repo):
    if(not os.path.exists(dir+'/.git')):
        os.system("git clone %s %s"%(repo['url'],dir))
    branch =  repo['branch']  if 'branch' in repo.keys() else ''
    version = repo['version']  if 'version' in repo.keys() else ''
    os.system("cd %s && git pull --rebase && git checkout %s %s"%(dir,branch,version))

def init_update_repo(config):
    repo = os.path.abspath(os.getcwd())
    update_repo('llvm',config['llvm'])
    os.chdir(r'llvm/tools')
    update_repo('clang',config['clang'])
    os.chdir(r'clang/tools')
    update_repo('extra',config['extra'])
    os.chdir(repo)

def generate_prj(generate):
    repo = os.path.abspath(os.getcwd())
    build_dir = generate['dir'] if 'dir' in generate.keys() else 'build'
    if(not os.path.exists(build_dir)):
        os.mkdir(build_dir)
    os.chdir(build_dir)

    gen_prj_command = ['cmake']
    if 'generator' in generate.keys():
        gen_prj_command.append('-G \"%s\"'%(generate['generator']))
    if 'toolset' in generate.keys():
        gen_prj_command.append('-T \"%s\"'%(generate['toolset']))
    gen_prj_cmd = ' '.join(gen_prj_command) + ' %s'%(repo+'/llvm')
    print(gen_prj_cmd)
    os.system(gen_prj_cmd)
    os.chdir(repo)

def build_target(build,dir,target,version):
    repo = os.path.abspath(os.getcwd())
    os.chdir(dir)

    build_target_command = ['cmake --build .']
    if target != None and target != '':
        build_target_command.append('--target %s'%(target))
    elif 'target' in build.keys():
        build_target_command.append('--target %s'%(build['target']))
    if version != None and version != '':
        build_target_command.append('--config %s'%(version))
    elif 'version' in build.keys():
        build_target_command.append('--config %s'%(build['version']))
    print(' '.join(build_target_command))
    os.system(' '.join(build_target_command))
    os.chdir(repo)

def main():
    parser = argparse.ArgumentParser(description='Clone,update,build llvm/clang/extra with specified configuration')
    parser.add_argument('-update',action='store_true',
                        help='Update repository')
    parser.add_argument('-build',action='store_true',
                        help='Build repository')
    parser.add_argument('-generate',action='store_true',
                        help='Generate project')
    parser.add_argument('-config',metavar='Configuration files',default='config.json',
                        help='Configuration files')
    parser.add_argument('-target',default=None, help='Build target. Works only when the \'build\' option exists,'
                        'you can override the \'build/target\' options specified in the configuration file')
    parser.add_argument('-version',default=None, help='Build version. Works only when the \'build\' option exists,'
                        'you can override the \'build/version\' options specified in the configuration file')
    args = parser.parse_args()
    with open('config.json', 'r') as f:
        config = json.load(f)
        if(args.update):
            init_update_repo(config)
        generate=config['generate']
        if(args.generate):
            generate_prj(generate)
        if(args.build):
            build_dir = generate['dir'] if 'dir' in generate.keys() else 'build'
            build_target(config['build'],build_dir,args.target,args.version)

if __name__ == '__main__':
    main()
    
