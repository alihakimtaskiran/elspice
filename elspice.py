import numpy as np


class Circuit(object):
    def __init__(self, dim):
        if not type(dim)==int:
            raise TypeError("Number of dimensions must be an integer")
        if dim<1:
            raise ValueError("Number of dimensions must be greater than 0")
        self.__dim = dim
        
    def manual(self):
        print("All Assets:\n\t(N,...,M):location\n\tV:Voltage Source\n\tI:DC Current Source\n\t-:Wire\n\tR:Resistor\n\tC:Capacitor\n\tL:Inductor\nFirstly, specify first point of connection, then second point of connection, after that component type,finally  SI units value.\nEx:\n\t(0,0) (1,1) -;\n\t(1,1) (2,2) R 5K;(2,2) (0,0) I 5;\nMake sure that there is one space between each property and there is semicolon between each components")
    
    def __check_syntax(self):
        return True
    @staticmethod
    def __convert_to_float(s):
        if s[-1] in {".","0","1","2","3","4","5","6","7","8","9"}:
            suffix=None
            return float(s)
        else:
            suffix = s[-1]
            number = float(s[:-1])
        if suffix == 'q':
            return number * 1e-30
        elif suffix == 'r':
            return number * 1e-27
        elif suffix == 'y':
            return number * 1e-24
        elif suffix == 'z':
            return number * 1e-21
        elif suffix == 'a':
            return number * 1e-18
        elif suffix == 'f':
            return number * 1e-15
        elif suffix == 'p':
            return number * 1e-12
        elif suffix == 'n':
            return number * 1e-9
        elif suffix == 'u':
            return number * 1e-6
        elif suffix == 'm':
            return number * 1e-3
        elif suffix == 'K':
            return number * 1e3
        elif suffix == 'M':
            return number * 1e6
        elif suffix == 'G':
            return number * 1e9
        elif suffix == 'T':
            return number * 1e12
        elif suffix == 'P':
            return number * 1e15
        elif suffix == 'E':
            return number * 1e18
        elif suffix == 'Z':
            return number * 1e21
        elif suffix == 'Y':
            return number * 1e24
        elif suffix == 'R':
            return number * 1e27
        elif suffix == 'Q':
            return number * 1e30
        else:
            raise ValueError(f"Suffix:{suffix} is not standardized")
    @staticmethod
    def __voltage_unit_string(value):
        if value < 1e-35:
            return "0 V"
        elif value < 1e-27:
            return str(value * 1e30) + " qV"
        elif value < 1e-24:
            return str(value * 1e27) + " rV"
        elif value < 1e-21:
            return str(value * 1e24) + " yV"
        elif value < 1e-18:
            return str(value * 1e21) + " zV"
        elif value < 1e-15:
            return str(value * 1e18) + " aV"
        elif value < 1e-12:
            return str(value * 1e15) + " fV"
        elif value < 1e-9:
            return str(value * 1e12) + " pV"
        elif value < 1e-6:
            return str(value * 1e9) + " nV"
        elif value < 1e-3:
            return str(value * 1e6) + " uV"
        elif value < 1:
            return str(value * 1e3) + " mV"
        elif value < 1e3:
            return str(value) + " V"
        elif value < 1e6:
            return str(value * 1e-3) + " KV"
        elif value < 1e9:
            return str(value * 1e-6) + " MV"
        elif value < 1e12:
            return str(value * 1e-9) + " GV"
        elif value < 1e15:
            return str(value * 1e-12) + " TV"
        elif value < 1e18:
            return str(value * 1e-18) + " PV"
        elif value < 1e21:
            return str(value * 1e-21) + " EV"
        elif value < 1e24:
            return str(value * 1e-24) + " ZV"
        elif value < 1e27:
            return str(value * 1e-27) + " YV"
        else:
            return str(value * 1e-30) + " QV"
        
    @staticmethod
    def __arg(num):
        return np.math.degrees(np.math.atan2(num.imag,num.real))
        
    def __Z(self,typ, val):
        if typ=="-":
            return 1e-39
        elif typ=="R":
            return val
        elif typ=="C":
            return -1j/self.__ac_omega/val
        elif typ=="L":
            return 1j*self.__ac_omega*val
        elif typ=="V":
            return val
        elif typ=="I":
            return val
        
        else:
            raise ValueError(f"Undefined component type:{typ}")
            
    @property
    def graph(self):
        return self.__graph
        
    def decode(self, code, frequency=0):
        self.__check_syntax()
        self.__ac_omega=2*np.pi*frequency
        self.__pre_set=code.replace("\n","").split(";")
        self.__graph={}
        for i in range(len(self.__pre_set)):
            if self.__pre_set[i]!="":
                self.__pre_set[i]=self.__pre_set[i].split(" ")
                self.__pre_set[i][0]=tuple(map(int, self.__pre_set[i][0].strip('()').split(',')))
                self.__pre_set[i][1]=tuple(map(int, self.__pre_set[i][1].strip('()').split(',')))
                if self.__pre_set[i][-1]!="-":
                    self.__pre_set[i][-1]=self.__convert_to_float(self.__pre_set[i][-1])
                else:
                    self.__pre_set[i].append(0)
                
                    
                    
                for j in range(2):

                    if self.__pre_set[i][2]=="V":
                        sign=(j-.5)*2
                    elif self.__pre_set[i][2]=="I":
                        sign=(j-.5)*-2
                    else:
                        sign=1.

                    if self.__pre_set[i][j] not in self.__graph:
                        self.__graph[self.__pre_set[i][j]]=[(self.__pre_set[i][1-j],self.__pre_set[i][2],sign*self.__Z(self.__pre_set[i][2],self.__pre_set[i][3]))]
                    else:
                        self.__graph[self.__pre_set[i][j]].append((self.__pre_set[i][1-j],self.__pre_set[i][2],sign*self.__Z(self.__pre_set[i][2],self.__pre_set[i][3])))
        A,b=self.__linear_system()
        self.__lin_sys=A,b
        self.__node_voltages=np.linalg.inv(A)@b
  
    def __linear_system(self):
        num_unk=len(self.__graph)-1
        A=np.zeros((num_unk, num_unk),dtype="complex128")
        b=np.zeros(num_unk,dtype="complex128")
        ref=next(iter(self.__graph))
        self.__ref=ref
        self.__ind_map={}
        self.__rev_ind_map={}
        i=0;
        for node in self.__graph:
            self.__ind_map[i]=node
            self.__rev_ind_map[node]=i
            i+=1
        for i in range(1,len(self.__ind_map)):
            for connecto in self.__graph[self.__ind_map[i]]:
                if connecto[1]=="R" or connecto[1]=="L" or connecto[1]=="C" or connecto[1]=="-": 
                    A[i-1 , i-1]+=1/connecto[2]
                    if connecto[0]!=ref:
                        A[i-1 , self.__rev_ind_map[connecto[0]]-1]-=1/connecto[2]
                elif connecto[1]=="V":
                    A[i-1 , i-1]+=1e39
                    if connecto[0]!=ref:
                        A[i-1 , self.__rev_ind_map[connecto[0]]-1]-=1e39
                    b[i-1]+=connecto[2]*1e39
                elif connecto[1]=="I":
                    b[i-1]-=connecto[2]
                    
        return A,b
    
    @property
    def linear_system(self):
        return self.__lin_sys
    
    def nodes(self):
        print(f"Node Voltages:\n{next(iter(self.__graph))}: 0V 0°")
        for i in range(1,len(self.__ind_map)):
            if self.__ac_omega!=0:
                print(f"{self.__ind_map[i]}: {self.__voltage_unit_string(abs(self.__node_voltages[i-1]))}  {self.__arg(self.__node_voltages[i-1])} °")              
            else:
                if self.__node_voltages[i-1]<0:
                    sign="-"
                else:
                    sign=""
                print(f"{self.__ind_map[i]}: {sign}{self.__voltage_unit_string(abs(self.__node_voltages[i-1]))}")              

    def node_v(self, val):
        if val==self.__ref:
            return 0
        else:
            return self.__node_voltages[self.__rev_ind_map[val]]
    
    @property
    def node_voltages(self):
        return np.concatenate((np.array((0,)),self.__node_voltages)),self.__ind_map
