#!/usr/bin/env bash

# (foo/bar/)*(koeth_y)?(a_small)(.0)*.bmp
name=`echo $1 | sed -nE 's/(.*\/)*([a-z0-9-]{5}_[a-z]-)?([a-z0-9_]+)[.0-9-]*\.(bmp|png|jpg)$/\3/p' | tr -d '\n'`

# Test
#name=`echo $1 | sed -nE 's/(.*\/)*test_([0-9]).(bmp|png|jpg)/\2/p'`

if [ -z $name ]; then exit 1; fi

#import ocr
#folder = ocr.OCR.generateFolderList(ocr.OCR.DIGITS | ocr.OCR.SYMBOLS | ocr.OCR.LETTERS)
#for k, v in sorted(folderlist.iteritems()):
#  print "elif [ $name = '{0}' ]; then name='{1}';".format(v[8:], re.escape(k))

if [ $name = 'sym_exclmark' ]; then name='!';
elif [ $name = 'sym_quotmark' ]; then name='"';
elif [ $name = 'sym_num' ]; then name='#';
elif [ $name = 'sym_dollar' ]; then name='$';
elif [ $name = 'sym_pcent' ]; then name='%';
elif [ $name = 'sym_amper' ]; then name='&';
elif [ $name = 'sym_apos' ]; then name="'";
elif [ $name = 'sym_lparen' ]; then name='(';
elif [ $name = 'sym_rparen' ]; then name=')';
elif [ $name = 'sym_star' ]; then name='*'; 
elif [ $name = 'sym_plus' ]; then name='+'; 
elif [ $name = 'sym_comma' ]; then name=','; 
elif [ $name = 'sym_hyphen' ]; then name='-'; 
elif [ $name = 'sym_point' ]; then name='.'; 
elif [ $name = 'sym_slash' ]; then name='/'; 
elif [ $name = 'sym_space' ]; then name=' ';
elif [ $name = 'num_0' ]; then name='0'; 
elif [ $name = 'num_1' ]; then name='1'; 
elif [ $name = 'num_2' ]; then name='2'; 
elif [ $name = 'num_3' ]; then name='3'; 
elif [ $name = 'num_4' ]; then name='4'; 
elif [ $name = 'num_5' ]; then name='5'; 
elif [ $name = 'num_6' ]; then name='6'; 
elif [ $name = 'num_7' ]; then name='7'; 
elif [ $name = 'num_8' ]; then name='8'; 
elif [ $name = 'num_9' ]; then name='9'; 
elif [ $name = 'sym_colon' ]; then name=':'; 
elif [ $name = 'sym_scolon' ]; then name=';'; 
elif [ $name = 'sym_lthan' ]; then name='<'; 
elif [ $name = 'sym_equal' ]; then name='='; 
elif [ $name = 'sym_gthan' ]; then name='>'; 
elif [ $name = 'sym_questmark' ]; then name='?'; 
elif [ $name = 'sym_arob' ]; then name='@'; 
elif [ $name = 'a' ]; then name='A'; 
elif [ $name = 'b' ]; then name='B'; 
elif [ $name = 'c' ]; then name='C'; 
elif [ $name = 'd' ]; then name='D'; 
elif [ $name = 'e' ]; then name='E'; 
elif [ $name = 'f' ]; then name='F'; 
elif [ $name = 'g' ]; then name='G'; 
elif [ $name = 'h' ]; then name='H'; 
elif [ $name = 'i' ]; then name='I'; 
elif [ $name = 'j' ]; then name='J'; 
elif [ $name = 'k' ]; then name='K'; 
elif [ $name = 'l' ]; then name='L'; 
elif [ $name = 'm' ]; then name='M'; 
elif [ $name = 'n' ]; then name='N'; 
elif [ $name = 'o' ]; then name='O'; 
elif [ $name = 'p' ]; then name='P'; 
elif [ $name = 'q' ]; then name='Q'; 
elif [ $name = 'r' ]; then name='R'; 
elif [ $name = 's' ]; then name='S'; 
elif [ $name = 't' ]; then name='T'; 
elif [ $name = 'u' ]; then name='U'; 
elif [ $name = 'v' ]; then name='V'; 
elif [ $name = 'w' ]; then name='W'; 
elif [ $name = 'x' ]; then name='X'; 
elif [ $name = 'y' ]; then name='Y'; 
elif [ $name = 'z' ]; then name='Z'; 
elif [ $name = 'sym_lsqbracket' ]; then name='['; 
elif [ $name = 'sym_bslash' ]; then name='\'; 
elif [ $name = 'sym_rsqbracket' ]; then name=']'; 
elif [ $name = 'sym_caret' ]; then name='^'; 
elif [ $name = 'sym_under' ]; then name='_'; 
elif [ $name = 'sym_bquote' ]; then name='`'; 
elif [ $name = 'a_small' ]; then name='a'; 
elif [ $name = 'b_small' ]; then name='b'; 
elif [ $name = 'c_small' ]; then name='c'; 
elif [ $name = 'd_small' ]; then name='d'; 
elif [ $name = 'e_small' ]; then name='e'; 
elif [ $name = 'f_small' ]; then name='f'; 
elif [ $name = 'g_small' ]; then name='g'; 
elif [ $name = 'h_small' ]; then name='h'; 
elif [ $name = 'i_small' ]; then name='i'; 
elif [ $name = 'j_small' ]; then name='j'; 
elif [ $name = 'k_small' ]; then name='k'; 
elif [ $name = 'l_small' ]; then name='l'; 
elif [ $name = 'm_small' ]; then name='m'; 
elif [ $name = 'n_small' ]; then name='n'; 
elif [ $name = 'o_small' ]; then name='o'; 
elif [ $name = 'p_small' ]; then name='p'; 
elif [ $name = 'q_small' ]; then name='q'; 
elif [ $name = 'r_small' ]; then name='r'; 
elif [ $name = 's_small' ]; then name='s'; 
elif [ $name = 't_small' ]; then name='t'; 
elif [ $name = 'u_small' ]; then name='u'; 
elif [ $name = 'v_small' ]; then name='v'; 
elif [ $name = 'w_small' ]; then name='w'; 
elif [ $name = 'x_small' ]; then name='x'; 
elif [ $name = 'y_small' ]; then name='y'; 
elif [ $name = 'z_small' ]; then name='z'; 
elif [ $name = 'sym_lcbracket' ]; then name='{'; 
elif [ $name = 'sym_pipe' ]; then name='|'; 
elif [ $name = 'sym_rcbracket' ]; then name='}'; 
elif [ $name = 'sym_tilde' ]; then name='~'; fi

echo -n "$name"
