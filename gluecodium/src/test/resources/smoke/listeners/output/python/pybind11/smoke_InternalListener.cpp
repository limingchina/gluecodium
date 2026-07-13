

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InternalListener.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalListener = ::gluecodium::smoke::InternalListener;

class InternalListenerTrampoline : public InternalListener {
public:
    using InternalListener::InternalListener;

    void on_event(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, InternalListener, on_event);
    }
};

void register_InternalListener(py::module_& module) {
    py::class_<InternalListener, std::shared_ptr<InternalListener>, InternalListenerTrampoline>(module, "InternalListener")
        .def(py::init<>())
        .def("on_event", &InternalListener::on_event)
        ;
}

