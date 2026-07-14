

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InternalInterfaceParent.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalInterfaceParent = ::smoke::InternalInterfaceParent;

class InternalInterfaceParentTrampoline : public InternalInterfaceParent {
public:
    using InternalInterfaceParent::InternalInterfaceParent;

    void foo_bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, InternalInterfaceParent, foo_bar);
    }
    ::std::string& get_prop() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, InternalInterfaceParent, get_prop);
    }
    void set_prop(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, InternalInterfaceParent, set_prop, value);
    }
};

void register_InternalInterfaceParent(py::module_& module) {
    py::class_<InternalInterfaceParent, std::shared_ptr<InternalInterfaceParent>, InternalInterfaceParentTrampoline>(module, "InternalInterfaceParent")
        .def(py::init<>())
        .def("foo_bar", [](InternalInterfaceParent& self) {
            return self.foo_bar();
        })
        .def_property("prop", py::overload_cast<>(&InternalInterfaceParent::get_prop, py::const_), py::overload_cast<const ::std::string&>(&InternalInterfaceParent::set_prop))
        ;
}

