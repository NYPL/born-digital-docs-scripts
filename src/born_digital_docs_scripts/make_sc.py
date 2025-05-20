from pathlib import Path
import logging
import subprocess 
import argparse
import re

# Accept a directory (could hardcode or argparse)
def parse_args() -> argparse.Namespace:
    def extant_path(p: str) -> Path:
        path = Path(p) 
        if not path.exists():
            raise argparse.ArgumentTypeError(f"{path} does not exist")
        return path
    
    # def rclone_remote(p: str) -> Path:
    #     if not re.match(r'*:*', p):
    #         raise argparse.ArgumentTypeError(f"{p} doesn't looke like an rclone remote")
    #     return p
    
    parser = argparse.ArgumentParser(description="path to a directory of born digital ami")
    parser.add_argument("--source", "-s", required=True, type=extant_path)
    parser.add_argument("--dest", "-d", required=True, type=str)
    return parser.parse_args()
    

# Function take directory (or staged excel), Find all EM files, return list
def get_em(path: Path) -> list[Path]:
    source = path
    ems = []
    for x in source.rglob("*_em.*"):
        if not str(x).endswith('mov'):
            print(f"is this okay?: {x}")
        else:
            ems.append(x)

    # print(ems)
    return ems


# Function takes list of EM files, find if interlaced or not, return list of [path, interlaced] → mediainfo (use Inform argument)
def find_interlace(path: list[Path]) -> list[list[Path,str]]:
    interlacing = subprocess.check_output(['mediainfo', 
                                "--Inform=Video;%ScanType%", 
                                path], 
                                encoding='utf-8').strip()
       


        #below for testing purposes
        # if len(str(path)) / 2 == 0: # just to create variation for now
        #     interlacing.append([path, 'interlaced'])
        # else:
        #     interlacing.append([path, 'progressive'])
    # print(interlacing)
    return path, interlacing


# Function take list of of [path, interlaced], create ffmpeg commands (need to adjust interlacing and service file path per command) (may need to create servicecopy folder before ffmpeg runs), return list of commands


# Overwrite servicecopies, may need to add flag to ffmpeg to do this (-y?)
def make_commands(file: list[list[Path,str]]) -> list[list[str]]:
    em_path = file[0]
    em_path_str = str(em_path)
    # PosixPath('test_ems/dir_3/data/EditMaster/sample_dig_3_em.mov')
    base = em_path.parent.parent
    '''
    May be useful to include a check for service copy directory already existing. 
    added because ffmpeg did not like the directory not already existing
    '''
    dest = base / 'ServiceCopies'
    subprocess.run(['mkdir', f'{dest}'])
    sc_path_str =  str(base / 'ServiceCopies' / em_path.name.replace("em.mov", "sc.mp4"))
    if file[1] == 'interlaced':
        cmd = ['ffmpeg', '-i', em_path_str, '-map', '0:v', '-map', '0:a', '-c:v', 'libx264', '-movflags', '+faststart', '-crf', '20', '-maxrate', '7.5M', '-bufsize', '7.5M', '-vf', 'yadif', '-c:a', 'aac', '-b:a', '320000', '-ar', '48000', sc_path_str]
    else:
        cmd = ['ffmpeg', '-i', em_path_str, '-map', '0:v', '-map', '0:a', '-c:v', 'libx264', '-movflags', '+faststart', '-crf', '20', '-maxrate', '7.5M', '-bufsize', '7.5M', '-c:a', 'aac', '-b:a', '320000', '-ar', '48000', sc_path_str]


    return cmd



# # Function take list of commands, run each command, return list of sc files
def make_sc(command: list[list[str]]) -> list[str]:
    # logging.DEBUG(f"Running this command {c}")
    subprocess.run(command)
    sc = command[-1]
    logging.info(f"{command[-1]} created")
 
    return sc

# # Function take list of sc files, make rclone command, return list of commands
def make_rclone(file: str, dest: str) -> list[list[str]]:
    fn = Path(file).name
    rc = ['rclone', 'copyto', file, f'{dest}/{fn}', '-P']

    # print(commands)
    return rc
        
# # Function take list of rclone commands, run each, return none
def run_rclone(command: list[str]) -> None:
    logging.info(f"transferring {command[2]}")
    subprocess.run(command)
    logging.info(f"{command[2]} has been transferred")

    return None

def main():
    source = parse_args().source
    dest = parse_args().dest
    ems = get_em(source)
    for em in ems:
        em_path = find_interlace(em)
        ff_cmds = make_commands(em_path)
        if Path(ff_cmds[-1]).exists():
             continue
        print(em, ff_cmds[-1])
        if not str(em.name).startswith('myd'):
             continue
        sc = make_sc(ff_cmds)
        rc_cmds = make_rclone(ff_cmds[-1],dest)

        run_rclone(rc_cmds)
    # sc
   
    # for cmd in ff_cmds:
    #     print(cmd[-1])


  


if __name__ == "__main__":
    main()    
