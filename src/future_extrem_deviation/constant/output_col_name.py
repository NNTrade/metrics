from ..extrem_type import ExtreamType

def get_value_col(extrem_type:ExtreamType, use_base_names:bool = False)->str:
  return EXTREM_OF_BASE if use_base_names else f"{EXTREM_OF_BASE}_of_{extrem_type.name}"

def get_idx_col(extrem_type:ExtreamType, use_base_names:bool = False)->str:
  return IDX_OF_BASE if use_base_names else f"{IDX_OF_BASE}_of_{extrem_type.name}"

def get_shift_col(extrem_type:ExtreamType, use_base_names:bool = False)->str:
  return SHIFT_OF_BASE if use_base_names else f"{SHIFT_OF_BASE}_to_{extrem_type.name}"

def get_rel_col(extrem_type:ExtreamType, use_base_names:bool = False)->str:
  return REL_OF_BASE if use_base_names else f"{REL_OF_BASE}_of_{extrem_type.name}"

EXTREM_OF_BASE = "Extrem"
EXTREM_OF_HIGH = get_value_col(ExtreamType.High)
EXTREM_OF_LOW = get_value_col(ExtreamType.Low)

IDX_OF_BASE = "Idx"
IDX_OF_HIGH = get_idx_col(ExtreamType.High)
IDX_OF_LOW = get_idx_col(ExtreamType.Low)

SHIFT_OF_BASE = "Shift"
SHIFT_OF_HIGH = get_shift_col(ExtreamType.High)
SHIFT_OF_LOW = get_shift_col(ExtreamType.Low)

REL_OF_BASE = "Rel"
REL_OF_HIGH = get_rel_col(ExtreamType.High)
REL_OF_LOW = get_rel_col(ExtreamType.Low)