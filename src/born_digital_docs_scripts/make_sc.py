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
def find_interlace(paths: list[Path]) -> list[list[Path,str]]:
    interlacing = []
    for path in paths:
        # mediainfo results = subprocess.
        # if mediainfo_result == ...
        # mediainfo --Output="Video;%ScanType%"
        mediainfo = subprocess.check_output(['mediainfo', 
                                    "--Inform=Video;%ScanType%", 
                                    path], 
                                    encoding='utf-8').strip()
       
        interlacing.append([path,mediainfo])

        #below for testing purposes
        # if len(str(path)) / 2 == 0: # just to create variation for now
        #     interlacing.append([path, 'interlaced'])
        # else:
        #     interlacing.append([path, 'progressive'])
    # print(interlacing)
    return interlacing


# Function take list of of [path, interlaced], create ffmpeg commands (need to adjust interlacing and service file path per command) (may need to create servicecopy folder before ffmpeg runs), return list of commands


# Overwrite servicecopies, may need to add flag to ffmpeg to do this (-y?)
def make_commands(files: list[list[Path,str]]) -> list[list[str]]:
    commands = []

    for x in files:
        em_path = x[0]
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
        if x[1] == 'interlaced':
            cmd = ['ffmpeg', '-i', em_path_str, '-map', '0:v', '-map', '0:a', '-c:v', 'libx264', '-movflags', '+faststart', '-crf', '20', '-maxrate', '7.5M', '-bufsize', '7.5M', '-vf', 'yadif', '-c:a', 'aac', '-b:a', '320000', '-ar', '48000', sc_path_str]
        else:
            cmd = ['ffmpeg', '-i', em_path_str, '-map', '0:v', '-map', '0:a', '-c:v', 'libx264', '-movflags', '+faststart', '-crf', '20', '-maxrate', '7.5M', '-bufsize', '7.5M', '-c:a', 'aac', '-b:a', '320000', '-ar', '48000', sc_path_str]

        commands.append(cmd)

    return commands



# # Function take list of commands, run each command, return list of sc files
def make_sc(commands: list[list[str]]) -> list[str]:
    sc = []
    for c in commands:
        # logging.DEBUG(f"Running this command {c}")
        subprocess.run(c)
        sc.append(c[-1])
        logging.info(f"{c[-1]} created")
 
    return sc

# # Function take list of sc files, make rclone command, return list of commands
def make_rclone(files: list[str], dest) -> list[list[str]]:
    commands = []
    
    for sc in files:
        fn = Path(sc).name
        print(fn)
        rc = ['rclone', 'copyto', sc, f'{dest}/{fn}', '-P']
        commands.append(rc)

    # print(commands)
    return commands
        
# # Function take list of rclone commands, run each, return none
def run_rclone(commands: list[list[str]]) -> None:
    for c in commands:
        print(c)
        logging.info(f"transferring {c[2]}")
        subprocess.run(c)
        logging.info(f"{c[2]} has been transferred")

    return None

def main():
    source = parse_args().source
    dest = parse_args().dest
    ems = get_em(source)
    em_paths = find_interlace(ems)
    ff_cmds = make_commands(em_paths)
    sc = make_sc(ff_cmds)
    rc_cmds = make_rclone(sc,dest)

    run_rclone(rc_cmds)
    # sc
   
    # for cmd in ff_cmds:
    #     print(cmd[-1])


  


if __name__ == "__main__":
    main()    