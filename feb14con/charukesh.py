import sqlite3
from anytree import Node,RenderTree,search
c=sqlite3.connect('connnew.db', check_same_thread=False)
cursor=c.cursor()
# cursor.execute('DROP TABLE details')
# cursor.execute("""CREATE TABLE details (
#     id char(6) NOT NULL PRIMARY KEY,
#     password char(20) NOT NULL,
#     name char(30) NOT NULL,
#     qualification char(30) NOT NULL,
#     insta char(50) NOT NULL,
#     fb char(50),
#     tweet char(50));""")
# cursor.execute('DROP TABLE contacts')
# cursor.execute("""CREATE TABLE contacts(
#     id char(6) NOT NULL PRIMARY KEY,
#     c1 char(6) NOT NULL,
#     c2 char(6),
#     c3 char(6),
#     c4 char(6),
#     c5 char(6),
#     c6 char(6),
#     c7 char(6),
#     c8 char(6),
#     c9 char(6),
#     c10 char(6),
#     c11 char(6),
#     c12 char(6),
#     c13 char(6),
#     c14 char(6),
#     c15 char(6),
#     c16 char(6),
#     c17 char(6),
#     c18 char(6),
#     c19 char(6),
#     c20 char(6));""")
# # cursor.execute('DROP TABLE id_detail')
# cursor.execute("""CREATE TABLE id_detail (
#     insta char(50),
#     id char(6));""")
cc=-1
# # cursor.execute('DROP TABLE y')
# cursor.execute("CREATE TABLE y(value int);")
# cursor.execute("INSERT INTO y VALUES(65535)")
class details:
    #To enter values into details table
    def into_values(self,name,passwd,q,insta,fb,tweet):
        id_=self.id_generator(insta)
        if fb==tweet==None:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}",NULL,NULL);"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta)
        elif fb==None:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}",NULL,"{tweet}");"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta,tweet=tweet)
        elif tweet==None:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}","{fb}",NULL);"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta,fb=fb)
        else:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}","{fb}","{tweet}");"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta,fb=fb,tweet=tweet)
        cursor.execute(sql)
        return id
    #to get values from details table with id
    def get_value(self,id_):
        cursor.execute("""SELECT id,name,qualification,insta,fb,tweet FROM details WHERE (id="{id_}");""".format(id_=id_))
        data=cursor.fetchall()
        return data
    #To generate or get id for insta
    def id_generator(self,insta):
        cursor.execute("""SELECT id FROM id_detail WHERE (insta="{insta}");""".format(insta=insta))
        z=cursor.fetchall()
        x=[]
        if(z==[]):
            cursor.execute("SELECT * FROM y")
            y=cursor.fetchall()
            yy=y[0]
            x.append(str(hex(yy[0])))
            yy=list(yy)
            yy[0]-=1
            cursor.execute("""INSERT INTO id_detail VALUES("{insta}","{x}");""".format(insta=insta,x=x[0]))
            cursor.execute("UPDATE y SET value={a} WHERE value={b}".format(a=yy[0],b=yy[0]+1))
        else:
            x=z[0]
        return x[0]
    #to store contacts
    def into_contact(self,u_insta,c_insta):
        c_list=[]
        k=0
        id_=self.id_generator(u_insta)
        for j in c_insta:
            c_list.append(self.id_generator(j))
            k+=1
        if k!=20:
            while(k!=20):
                c_list.append(None)
                k+=1
        string="""INSERT INTO contacts VALUES("{id_}","{a}","{b}","{c}","{d}","{e}","{f}","{i}","{j}"
                  ,"{k}","{l}","{m}","{n}","{o}","{p}","{q}","{r}","{s}","{t}","{u}","{v}");"""
        cursor.execute(string.format(id_=id_,a=c_list[0],b=c_list[1],c=c_list[2],d=c_list[3],e=c_list[4],f=c_list[5],i=c_list[6],j=c_list[7],k=c_list[8],l=c_list[9],
        m=c_list[10],n=c_list[11],o=c_list[12],p=c_list[13],q=c_list[14],r=c_list[15],s=c_list[16],t=c_list[17],u=c_list[18],v=c_list[19]))
        return 1
    #To find the contacts from person 1 to person 2
    def find_contact(self,id_1,id_2,c):
        child=[]
        child.append(Node(id_2))
        count=1
        check=[id_2]
        #print("check: ",check)
        note=0
        i=0
        l=0
        while note<=c:
            cursor.execute("""SELECT id FROM contacts WHERE (c1="{id2}" OR c2="{id2}" OR c3="{id2}" OR
                          c4="{id2}" OR c5="{id2}" OR c6="{id2}" OR c7="{id2}" OR c8="{id2}" OR 
                          c9="{id2}" OR c10="{id2}" OR c11="{id2}" OR c12="{id2}" OR c13="{id2}" OR
                          c14="{id2}" OR c15="{id2}" OR c16="{id2}" OR c17="{id2}" OR c18="{id2}" OR
                          c19="{id2}" OR c20="{id2}");""".format(id2=check[l]))
            l+=1
            x=cursor.fetchall()
            #for j in x:
            #    print("----",j)
            for j in x:
                if j[0] in check:
                    list(x).remove(j)
            for j in x:
                check.append(j[0])
            if id_1 in check:
                note+=1
                if(note<c+1):
                    for j in x:
                        if(j[0]==id_1):
                            x.remove(j)
                    check.remove(id_1)
            for j in x:
                child.append(Node(j[0],parent=child[i]))
            count+=1
            i+=1
            #print("check: ",check)
            print(RenderTree(child[0]))
            
        k=str(search.findall(child[0],filter_=lambda node: node.name in (id_1))).split("/")
        result=[]
        for i in range(1,len(k)-1):
            result.append(k[i])
        g=k[len(k)-1]
        h=len(k[1])
        result.append(g[:h])
        return result
    def times(self,id_1,id_2):
        global cc
        cc+=1
        return self.find_contact(id_1,id_2,cc)





d=details()
# x=[]
# x.append(d.into_values('virat_kohli','hello@987','cricketer','virat.kohli','virat_fb','virat__official'))
# x.append(d.into_values('Rohit_sharma','jihu#234','cricketer','rohit.official','rohit_sharma',None))
# x.append(d.into_values('rishab_pant','ramobo$127','cricketer','rishab.pant',None,'rihab.official'))
# x.append(d.into_values('mahesh_babu','reo$2358','actor','urstruely_mahesh',None,None))
# x.append(d.into_values('bill_gates','juty#1278','business','bill.official','billgates','bill.official'))
# c.commit()
# #print(x)
# cursor.execute("""SELECT * FROM details""")
# h=cursor.fetchall()
# print('------------',h)
# cursor.execute("""SELECT * FROM id_detail""")
# u=cursor.fetchall()
# #print("-",u) 
# # for i in u:
# #     print(d.get_value(i[1])) 
# x=['rohit.official','rishab.pant']
# d.into_contact('virat.kohli',x)
# cursor.execute("""SELECT * FROM id_detail""")
# u=cursor.fetchall()
# #print("-",u)
# cursor.execute("""SELECT * FROM contacts""")
# u=cursor.fetchall()
# #print("$",u)

x=['@priyu11']
d.into_contact('miraoixx',x)
# cursor.execute("""SELECT * FROM id_detail""")
# u=cursor.fetchall()
# #print("----",u)
# cursor.execute("""SELECT * FROM contacts""")
# u=cursor.fetchall()
# #print("$",u)

# x=['urstruely_mahesh']
# d.into_contact('rishab.pant',x)
# cursor.execute("""SELECT * FROM id_detail""")
# u=cursor.fetchall()
# #print("----",u)
# cursor.execute("""SELECT * FROM contacts""")
# u=cursor.fetchall()
# #print("$",u)

# x=['bill.official']
# d.into_contact('urstruely_mahesh',x)
# cursor.execute("""SELECT * FROM id_detail""")
# u=cursor.fetchall()
# #print("----",u)
# x=['insta123']
# d.into_contact('bill.official',x)

# cursor.execute("""SELECT * FROM contacts""")
# u=cursor.fetchall()
# print("$",u)

# x=d.times('0xffff','0xfffa')
# print(x)
# x=d.times('0xffff','0xfffa')
# print(x)
c.commit() 
