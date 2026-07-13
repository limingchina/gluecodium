

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ListenerInterface.h"
#include "smoke/Weakling.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Weakling = ::gluecodium::smoke::Weakling;

class WeaklingTrampoline : public Weakling {
public:
    using Weakling::Weakling;

    ::std::shared_ptr< ::smoke::ListenerInterface >& get_listener() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::shared_ptr< ::smoke::ListenerInterface >&, Weakling, get_listener);
    }
    void set_listener(const ::std::shared_ptr< ::smoke::ListenerInterface >& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, Weakling, set_listener, value);
    }
};

void register_Weakling(py::module_& module) {
    py::class_<Weakling, std::shared_ptr<Weakling>, WeaklingTrampoline>(module, "Weakling")
        .def_property("listener", py::overload_cast<>(&Weakling::get_listener, py::const_), py::overload_cast<const ::std::shared_ptr< ::smoke::ListenerInterface >&>(&Weakling::set_listener))
        ;
}

