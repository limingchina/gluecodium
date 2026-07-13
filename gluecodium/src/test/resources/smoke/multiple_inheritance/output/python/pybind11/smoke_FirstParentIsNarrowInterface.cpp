

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FirstParentIsNarrowInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsNarrowInterface = ::smoke::FirstParentIsNarrowInterface;

class FirstParentIsNarrowInterfaceTrampoline : public FirstParentIsNarrowInterface {
public:
    using FirstParentIsNarrowInterface::FirstParentIsNarrowInterface;

    void child_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, FirstParentIsNarrowInterface, child_function);
    }
    ::std::string& get_child_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, FirstParentIsNarrowInterface, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, FirstParentIsNarrowInterface, set_child_property, value);
    }
};

void register_FirstParentIsNarrowInterface(py::module_& module) {
    py::class_<FirstParentIsNarrowInterface, std::shared_ptr<FirstParentIsNarrowInterface>, FirstParentIsNarrowInterfaceTrampoline>(module, "FirstParentIsNarrowInterface")
        .def(py::init<>())
        .def("child_function", &FirstParentIsNarrowInterface::child_function)
        .def_property("child_property", py::overload_cast<>(&FirstParentIsNarrowInterface::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsNarrowInterface::set_child_property))
        ;
}

