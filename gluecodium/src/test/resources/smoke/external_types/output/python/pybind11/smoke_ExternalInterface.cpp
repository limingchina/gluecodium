

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExternalInterface = ::smoke::ExternalInterface;

class ExternalInterfaceTrampoline : public ExternalInterface {
public:
    using ExternalInterface::ExternalInterface;

    void some_Method(
            int8_t some_parameter ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ExternalInterface, some_Method, some_parameter);
    }
    ::std::string& get_Me() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, ExternalInterface, get_Me);
    }
};

void register_ExternalInterface(py::module_& module) {
    py::class_<ExternalInterface, std::shared_ptr<ExternalInterface>, ExternalInterfaceTrampoline>(module, "ExternalInterface")
        .def(py::init<>())
        .def("some_method", &ExternalInterface::some_Method, py::arg("some_parameter"))
        .def_property_readonly("some_property", py::overload_cast<>(&ExternalInterface::get_Me, py::const_))
        ;
}

