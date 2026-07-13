

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ListenerInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ListenerInterface = ::gluecodium::smoke::ListenerInterface;

class ListenerInterfaceTrampoline : public ListenerInterface {
public:
    using ListenerInterface::ListenerInterface;

    void notify(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ListenerInterface, notify);
    }
};

void register_ListenerInterface(py::module_& module) {
    py::class_<ListenerInterface, std::shared_ptr<ListenerInterface>, ListenerInterfaceTrampoline>(module, "ListenerInterface")
        .def("notify", &ListenerInterface::notify)
        ;
}

