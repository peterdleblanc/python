__author__ = 'Peter LeBlanc'

import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import  ColumnFamily


def main():

    pool = ConnectionPool('Testing', ['localhost:9160'])
    users = ColumnFamily(pool, 'users')

    #users.insert('pleblanc', {'first_name':'Peter', 'last_name':'LeBlanc', 'status':'active'})

    userRecord = users.get('pleblanc')

    print userRecord



    #col_fam.get('row key')
    #{'col_name': 'col_val', 'col_name2': 'col_val2'}



if __name__ == '__main__':
    main()
    
