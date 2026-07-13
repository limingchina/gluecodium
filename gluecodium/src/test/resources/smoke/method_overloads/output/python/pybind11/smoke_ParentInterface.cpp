

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentInterface.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentInterface = ::gluecodium::smoke::ParentInterface;

class ParentInterfaceTrampoline : public ParentInterface {
public:
    using ParentInterface::ParentInterface;

    void foo(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterface, foo);
    }
    void foo(
            int32_t input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterface, foo, input);
    }
    void bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterface, bar);
    }
    void baz(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterface, baz);
    }
};

void register_ParentInterface(py::module_& module) {
    py::class_<ParentInterface, std::shared_ptr<ParentInterface>, ParentInterfaceTrampoline>(module, "ParentInterface")
        .def(py::init<>())
        .def("foo", &ParentInterface::foo)
        .def("foo", &ParentInterface::foo, py::arg("input"))
        .def("bar", &ParentInterface::bar)
        .def("baz", &ParentInterface::baz)
        ;
}

