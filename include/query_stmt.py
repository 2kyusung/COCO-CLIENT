import include.log as log
import re

class QueryStmt:
	# readonly
	# types = ['i', 's', 'j'] # i: 숫자, s: 문자, j:injection문자열 제외 ; -- OR AND | ' = ( ) # "
	
	# # instance value
	# query = None
	# cnt = 0
	# values = []

	# debug = False
	# singleton = None
	
	# def __init__ (self, query = ''):
	# 	if query:
	# 		self.prototype(query)
	
	# static public function safe($query, $binding_args = array())
	# {
	# 	if(!is_array($binding_args)) $binding_args = array($binding_args);
	
	# 	if(self::$singleton == null)
	# 		self::$singleton = new QueryStmt();
			
	# 	self::$singleton->prototype($query);
	# 	foreach($binding_args as $v)
	# 	{
	# 		$type = 's';
	# 		if( is_array($v) )
	# 		{
	# 			$type = key($v);
	# 			$val = $v[$type];
	# 		}
	# 		else
	# 		{
	# 			$val = $v;
	# 		}

	# 		self::$singleton->bind($type, $val);
	# 	}
	# 	return self::$singleton->build();
	# }
	
	# def init(self):
	# 	QueryStmt.query = None
	# 	QueryStmt.cnt = 0
	# 	QueryStmt.values = []
	
	# def prototype($query)
	# {
	# 	$this->init();
		
	# 	// query에는 '?'형태로 들어오면 안됨.
	# 	$p = strpos($query, "'?'");
	# 	if($p !== false) self::occured_error('invalid query prototype');

	# 	// ?의 갯수를 카운팅함.
	# 	$this->cnt = substr_count($query, '?');
		
		
	# 	$this->query = $query;
	# }
	
	@classmethod
	def addslashes(self, val, sub=re.compile(r"[\\\"']").sub):
		def fixup(m):
			return "\\" + m.group(0)
		return sub(fixup, val)

	

	# value검사 직접 query를 조합하는 곳에서도 사용하기 위해서 static으로 제공함.
	@classmethod
	def check_value(self, type, val, offset = None):
		try:
			if type == 's':
				val = QueryStmt.addslashes(val)
			elif type == 'i':
				try:
					float(val)
				except Exception as e:
					err_msg = 'invalid binding value'
					if offset != None:
						err_msg += F': offset={offset}'
					QueryStmt.occured_error(err_msg)
		except Exception as e:
			log.printException()
		return val
	
	# public function bind($type, $val)
	# {
	# 	if(in_array($type, $this->types) === false) self::occured_error('invalid binding type');
		
	# 	$offset = count($this->values);
		
	# 	$val = self::check_value($type, $val, $offset);
		
	# 	if($type == 's' || $type == 'j')
	# 		$val = "'${val}'";
	# 	else if($type == 'i')
	# 		$val = "${val}";

	# 	$this->values[] = $val;
		
	# 	if(count($this->values) > $this->cnt) self::occured_error('too many binding values');
	# }
	
	# public function build()
	# {
	# 	if(count($this->values) != $this->cnt) self::occured_error('insufficiency binding values');
		
	# 	$arr = explode('?', $this->query);
		
	# 	$arr2 = array();
	# 	foreach($arr as $v)
	# 	{
	# 		$arr2[] = $v;
	# 		$val = array_shift($this->values);
	# 		if($val !== null)
	# 		{
	# 			$arr2[] = $val;
	# 		}
	# 	}
		
	# 	$query = implode('', $arr2);
	# 	return $query;
	# }
	
	@classmethod
	def occured_error(self, msg):
		log.printLog(msg)
