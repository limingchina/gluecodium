

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FirstParentIsInterfaceInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsInterfaceInterface = ::smoke::FirstParentIsInterfaceInterface;

class FirstParentIsInterfaceInterfaceTrampoline : public FirstParentIsInterfaceInterface {
public:
    using FirstParentIsInterfaceInterface::FirstParentIsInterfaceInterface;

    void child_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, child_function);
    }
    ::std::string& get_child_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, FirstParentIsInterfaceInterface, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, FirstParentIsInterfaceInterface, set_child_property, value);
    }
};

void register_FirstParentIsInterfaceInterface(py::module_& module) {
    py::class_<FirstParentIsInterfaceInterface, std::shared_ptr<FirstParentIsInterfaceInterface>, FirstParentIsInterfaceInterfaceTrampoline>(module, "FirstParentIsInterfaceInterface")
        .def(py::init<>())
        .def("child_function", [](FirstParentIsInterfaceInterface& self) {
            return self.child_function();
        })
        .def_property("child_property", py::overload_cast<>(&FirstParentIsInterfaceInterface::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsInterfaceInterface::set_child_property))
        ;
}

