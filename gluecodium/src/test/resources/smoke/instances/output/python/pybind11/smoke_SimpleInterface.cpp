

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SimpleInterface.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SimpleInterface = ::gluecodium::smoke::SimpleInterface;

class SimpleInterfaceTrampoline : public SimpleInterface {
public:
    using SimpleInterface::SimpleInterface;

    ::std::string get_string_value(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string, SimpleInterface, get_string_value);
    }
    ::std::shared_ptr< ::smoke::SimpleInterface > use_simple_interface(
            const ::std::shared_ptr< ::smoke::SimpleInterface >& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::shared_ptr< ::smoke::SimpleInterface >, SimpleInterface, use_simple_interface, input);
    }
};

void register_SimpleInterface(py::module_& module) {
    py::class_<SimpleInterface, std::shared_ptr<SimpleInterface>, SimpleInterfaceTrampoline>(module, "SimpleInterface")
        .def(py::init<>())
        .def("get_string_value", &SimpleInterface::get_string_value)
        .def("use_simple_interface", &SimpleInterface::use_simple_interface, py::arg("input"))
        ;
}

