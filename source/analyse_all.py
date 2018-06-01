import os
import utils.launch_gen as launch

GENS = list(launch.GENS_DICT.keys())


def main():
    if os.path.exists('.\\gen.py'):
        for gen in GENS:
            os.system('mkdir .\\analysis\\{0}'.format(gen))
            os.system('gen.py /g:{0} /fout:.\\analysis\\{0}\\gen.txt /f:.\\analysis\\{0}\\rnd.dat'.format(gen))
            os.system('analysis.py /f:.\\analysis\\{0}\\rnd.dat /fout:.\\analysis\\{0}\\report.txt'.format(gen))
    else:
        for gen in GENS:
            os.system('mkdir .\\analysis\\{0}'.format(gen))
            os.system('gen.exe /g:{0} /fout:.\\analysis\\{0}\\gen_{0}.txt /f:.\\analysis\\{0}\\rnd_{0}.dat'.format(gen))
            os.system('analysis.exe /f:.\\analysis\\{0}\\rnd_{0}.dat /fout:.\\analysis\\{0}\\report_{0}.txt'.format(gen))


if __name__ == '__main__':
    main()
