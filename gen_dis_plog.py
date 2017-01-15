#!/usr/bin/env python

import sys
import shutil
import os
import subprocess

class DistrGen(object):

  def __init__(self):
    pass

  def __initpast__(self, plog_file = 'program_0.plog'):
    if os.path.isfile(plog_file) is False:
      print('p-log file does not exist: ' + plog_file)
      sys.exit()

    shutil.copy(plog_file, '/tmp')
    f = open('/tmp/' + plog_file, 'r')
    s = f.read()

    identity_list = ['alice', 'bob', 'carol']
    college_list=['engineering','education','bussiness']
    years_list=['seventies','eighties','nineties']
    mood_list = ['happy', 'sad']
    following_list = ['yes', 'no']

    output = ''

    for mood in mood_list:
      # print mood+'......'
      for fl in following_list:
        print( mood+'......' + fl + '......')
        output = ''
        for ident in identity_list:
          for coll in college_list:
            for year in years_list:
              query = '?{best_t(' + ident + ',' + coll + ',' + year + ')}'
              if fl is '':
                query += '.'
              else:
                query += '|obs(interest_m=' + mood + '),obs(interest_f=' + fl + '),do(last_table(bob,education,nineties)).'
              tmp_name = '/tmp/' + plog_file + '.tmp'
              with open(tmp_name, 'w') as ff:
                ff.write(s)
              with open(tmp_name, 'a') as ff:
                ff.write(query)

              out = subprocess.check_output('/home/ludc/workspace/context_aware_icorpp/plog/src/plog -t ' + tmp_name, shell = True)
              # print out
              out = out.split('\n')
              out = out[3]
              out = out.split(' ')
              out = out[3:]

              
              output += out[0] + ', '
              print(ident + '-' + coll + '-' + year + ': ' + out[0])
        print(output)

    f.close()

  def cal_belief(self, plog_file = 'guide.plog',\
                  mood= 'happy', \
                  fl='yes', \
                  curr_table='', \
                  last_table=''):
    if os.path.isfile(plog_file) is False:
      print('p-log file does not exist: ' + plog_file)
      sys.exit()

    shutil.copy(plog_file, '/tmp')
    f = open('/tmp/' + plog_file, 'r')
    s = f.read()

    identity_list = ['alice', 'bob', 'carol']
    college_list=['engineering','education','bussiness']
    years_list=['seventies','eighties','nineties']

    output = ''
    # print( mood+'......' + fl + '......')
    for ident in identity_list:
      for coll in college_list:
        for year in years_list:
          query = '?{best_t(' + ident + ',' + coll + ',' + year + ')}'
          if mood is '':
            if curr_table is not '':
              query += '|do(' + curr_table + ')'
              if last_table is not '':
                query += ',do(' + last_table + ')'
            else:
              if last_table is not '':
                query += '|do(' + last_table + ')'
            query += '.'
          else:
            query += '|obs(interest_m=' + mood + '),obs(interest_f=' + fl + ')'
            if curr_table is not '':
              query += ',do(' + curr_table + ')'
              if last_table is not '':
                query += ',do(' + last_table + ')'
            else:
              if last_table is not '':
                query += ',do(' + last_table + ')'
            query += '.'
          tmp_name = '/tmp/' + plog_file + '.tmp'
          with open(tmp_name, 'w') as ff:
            ff.write(s)
          with open(tmp_name, 'a') as ff:
            ff.write(query)

          out = subprocess.check_output('/home/ludc/workspace/context_aware_icorpp/plog/src/plog -t ' + tmp_name, shell = True)
          # print out
          out = out.split('\n')
          out = out[3]
          out = out.split(' ')
          out = out[3:]
          
          output += out[0] + ', '
          # print(ident + '-' + coll + '-' + year + ': ' + out[0])
    # print(output)

    output += '0'

    f.close()
    return output

def main():
  d = DistrGen(plog_file='guide.plog')
  subprocess.check_output('rm out.txt result.txt', shell = True)

if __name__ == '__main__':
  d = DistrGen()
  d.cal_belief(mood = 'happy', fl = 'yes', last_table = 'last_table(bob,education,nineties)')
  # main()
