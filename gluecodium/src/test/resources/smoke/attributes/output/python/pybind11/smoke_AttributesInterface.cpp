

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/AttributesInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AttributesInterface = ::smoke::AttributesInterface;

class AttributesInterfaceTrampoline : public AttributesInterface {
public:
    using AttributesInterface::AttributesInterface;

    void very_fun(
            const ::std::string& param ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, AttributesInterface, very_fun, param);
    }
    ::std::string& get_prop() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, AttributesInterface, get_prop);
    }
    void set_prop(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, AttributesInterface, set_prop, value);
    }
};

void register_AttributesInterface(py::module_& module) {
    py::class_<AttributesInterface, std::shared_ptr<AttributesInterface>, AttributesInterfaceTrampoline>(module, "AttributesInterface")
        .def(py::init<>())
        .def("very_fun", [](AttributesInterface& self, const ::std::string& param) {
            return self.very_fun(param);
        }, py::arg("param"))
        .def_property("prop", py::overload_cast<>(&AttributesInterface::get_prop, py::const_), py::overload_cast<const ::std::string&>(&AttributesInterface::set_prop))
        ;
}

