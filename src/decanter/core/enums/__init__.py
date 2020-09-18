"""Init jobs package"""
from .evaluators import Evaluator
from .algorithms import Algo

def check_is_enum(Enum, enum):
	if isinstance(enum, str):
		enum_isStr = eval('%s.%s'%(Enum.__name__, enum))
		if enum_isStr in Enum:
			return enum
		else:
			raise AttributeError(evaluator)
	elif isinstance(enum, Enum):
		return enum.value
	elif enum == None:
		return None
	else:
		raise AttributeError("[%s] Type Error"%type(enum).__name__)