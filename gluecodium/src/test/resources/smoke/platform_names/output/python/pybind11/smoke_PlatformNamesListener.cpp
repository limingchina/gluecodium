

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/fooListener.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PlatformNamesListener = ::gluecodium::smoke::PlatformNamesListener;

class PlatformNamesListenerTrampoline : public fooListener {
public:
    using fooListener::fooListener;

    void FooMethod(
            const ::std::string& basic_parameter ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, fooListener, FooMethod, basic_parameter);
    }
};

void register_PlatformNamesListener(py::module_& module) {
    py::class_<fooListener, std::shared_ptr<fooListener>, PlatformNamesListenerTrampoline>(module, "PlatformNamesListener")
        .def("basic_method", &fooListener::FooMethod, py::arg("basic_parameter"))
        ;
}

