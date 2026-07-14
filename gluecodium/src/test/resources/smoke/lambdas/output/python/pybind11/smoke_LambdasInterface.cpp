

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/LambdasInterface.h"
#include "cstdint"
#include "functional"
#include "memory"
#include "optional"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using LambdasInterface = ::smoke::LambdasInterface;

class LambdasInterfaceTrampoline : public LambdasInterface {
public:
    using LambdasInterface::LambdasInterface;

    void take_screenshot(
            const ::smoke::LambdasInterface::TakeScreenshotCallback& callback ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, LambdasInterface, take_screenshot, callback);
    }
};

void register_LambdasInterface(py::module_& module) {
    py::class_<LambdasInterface, std::shared_ptr<LambdasInterface>, LambdasInterfaceTrampoline>(module, "LambdasInterface")
        .def(py::init<>())
        .def("take_screenshot", [](LambdasInterface& self, const ::smoke::LambdasInterface::TakeScreenshotCallback& callback) {
            return self.take_screenshot(callback);
        }, py::arg("callback"))
        ;
}

