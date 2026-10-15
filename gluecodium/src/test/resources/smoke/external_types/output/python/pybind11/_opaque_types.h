
#pragma once

#include <pybind11/pybind11.h>
#include "core/duration.h"
#include "foo/Bar.h"
#include "foo/Bazz.h"
#include "gluecodium/VectorHash.h"
#include "include/ExternalTypeInTypesCollection.h"
#include "include/ExternalTypes.h"
#include "non/Sense.h"
#include "cstdint"
#include "string"
#include "vector"

// These types are registered as classes, rather than converted to STL values.
// All binding translation units must use the same caster specializations.
PYBIND11_MAKE_OPAQUE(::external::IntStruct);
PYBIND11_MAKE_OPAQUE(::fire::SomeVeryExternalStruct);
PYBIND11_MAKE_OPAQUE(::smoke::Structs::ExternalStruct);
PYBIND11_MAKE_OPAQUE(external::ClassWithOverloads::StructWithOverloads);
PYBIND11_MAKE_OPAQUE(std::chrono::duration<uint64_t, std::ratio<1,1000>>);
