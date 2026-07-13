

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipSetter.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipSetter = ::gluecodium::smoke::SkipSetter;

class SkipSetterTrampoline : public SkipSetter {
public:
    using SkipSetter::SkipSetter;

    ::std::string& get_foo() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, SkipSetter, get_foo);
    }
    void set_foo(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipSetter, set_foo, value);
    }
};

void register_SkipSetter(py::module_& module) {
    py::class_<SkipSetter, std::shared_ptr<SkipSetter>, SkipSetterTrampoline>(module, "SkipSetter")
        .def_property("foo", py::overload_cast<>(&SkipSetter::get_foo, py::const_), py::overload_cast<const ::std::string&>(&SkipSetter::set_foo))
        ;
}

