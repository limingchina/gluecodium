

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentInterfaceWithBool.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentInterfaceWithBool = ::gluecodium::smoke::ParentInterfaceWithBool;

class ParentInterfaceWithBoolTrampoline : public ParentInterfaceWithBool {
public:
    using ParentInterfaceWithBool::ParentInterfaceWithBool;

    void root_method(
            bool input1 ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterfaceWithBool, root_method, input1);
    }
};

void register_ParentInterfaceWithBool(py::module_& module) {
    py::class_<ParentInterfaceWithBool, std::shared_ptr<ParentInterfaceWithBool>, ParentInterfaceWithBoolTrampoline>(module, "ParentInterfaceWithBool")
        .def(py::init<>())
        .def("root_method", &ParentInterfaceWithBool::root_method, py::arg("input1"))
        ;
}

