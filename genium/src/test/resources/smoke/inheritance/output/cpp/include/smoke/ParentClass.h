// -------------------------------------------------------------------------------------------------
//
//
// -------------------------------------------------------------------------------------------------
#pragma once
#include "genium/Export.h"
#include "genium/TypeRepository.h"
namespace smoke {
class _GENIUM_CPP_EXPORT ParentClass {
public:
    ParentClass();
    virtual ~ParentClass() = 0;
public:
virtual void root_method(  ) = 0;
};
}
namespace genium {
_GENIUM_CPP_EXPORT TypeRepository& get_type_repository(const ::smoke::ParentClass*);
}
