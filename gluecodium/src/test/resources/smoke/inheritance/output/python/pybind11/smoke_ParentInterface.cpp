

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentInterface = ::gluecodium::smoke::ParentInterface;

class ParentInterfaceTrampoline : public ParentInterface {
public:
    using ParentInterface::ParentInterface;

    void root_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterface, root_method);
    }
    ::std::string& get_root_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, ParentInterface, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterface, set_root_property, value);
    }
};

void register_ParentInterface(py::module_& module) {
    py::class_<ParentInterface, std::shared_ptr<ParentInterface>, ParentInterfaceTrampoline>(module, "ParentInterface")
        .def(py::init<>())
        .def("root_method", &ParentInterface::root_method)
        .def_property("root_property", py::overload_cast<>(&ParentInterface::get_root_property, py::const_), py::overload_cast<const ::std::string&>(&ParentInterface::set_root_property))
        ;
}

