class Config():

    def __init__(self, pathConfig):

        try:
            with open(pathConfig, 'r') as f:
                configuracao = f.readlines()
            f.close()
            self.pathConfig = pathConfig

            self.User = str(configuracao[0]).strip('\n').strip('\r')
            self.Passwd = str(configuracao[1]).strip('\n').strip('\r')
            self.Host = str(configuracao[2]).strip('\n').strip('\r')
            self.Port = str(configuracao[3]).strip('\n').strip('\r')
            self.Db = str(configuracao[4]).strip('\n').strip('\r')
            self.Path = str(configuracao[5]).strip('\n').strip('\r')
            self.PathQ = str(configuracao[6]).strip('\n').strip('\r')
            self.Conn = "dbname='" + self.Db + "' user='" + self.User + "' host='" + self.Host \
                             + "' password='" + self.Passwd + "'"
            self.ConnUri = self.Host + ', ' + self.Port + ', ' + self.Db +', ' + self.User + \
                ', ' + self.Passwd

        except:
            print('classConstantes: Problema a ler config.ini. Programa terminado.')
            raise SystemExit

    def GravarConfig(self):
        resultado = False
        try:
            with open(self.pathConfig, 'w') as f:
                f.write(self.User + '\n')
                f.write(self.Passwd + '\n')
                f.write(self.Host + '\n')
                f.write(self.Port + '\n')
                f.write(self.Db + '\n')
                f.write(self.Path + '\n')
                f.write(self.PathQ + '\n')
            f.close()
            resultado = True
        except:
            print('classConstantes -----------------> erro ao gravar Config.ini !!!')
        finally:
            return resultado





