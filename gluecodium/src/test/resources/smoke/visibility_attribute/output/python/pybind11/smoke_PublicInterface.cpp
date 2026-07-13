

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PublicClass.h"
#include "smoke/PublicInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicInterface = ::gluecodium::smoke::PublicInterface;

class PublicInterfaceTrampoline : public PublicInterface {
public:
    using PublicInterface::PublicInterface;

};

void register_PublicInterface(py::module_& module) {
    py::class_<PublicInterface, std::shared_ptr<PublicInterface>, PublicInterfaceTrampoline>(module, "PublicInterface")
        ;
}

