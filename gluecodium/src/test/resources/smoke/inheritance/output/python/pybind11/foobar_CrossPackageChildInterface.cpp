

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foobar/CrossPackageChildInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CrossPackageChildInterface = ::foobar::CrossPackageChildInterface;

class CrossPackageChildInterfaceTrampoline : public CrossPackageChildInterface {
public:
    using CrossPackageChildInterface::CrossPackageChildInterface;

};

void register_CrossPackageChildInterface(py::module_& module) {
    py::class_<CrossPackageChildInterface, std::shared_ptr<CrossPackageChildInterface>, CrossPackageChildInterfaceTrampoline>(module, "CrossPackageChildInterface")
        .def(py::init<>())
        ;
}

