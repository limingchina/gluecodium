

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SpecialNamesInterface.h"
#include "functional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SpecialNamesInterface = ::smoke::SpecialNamesInterface;

class SpecialNamesInterfaceTrampoline : public SpecialNamesInterface {
public:
    using SpecialNamesInterface::SpecialNamesInterface;

    void dispatch(
            const ::smoke::SpecialNamesInterface::Callback& callback ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, SpecialNamesInterface, dispatch, callback);
    }
};

void register_SpecialNamesInterface(py::module_& module) {
    py::class_<SpecialNamesInterface, std::shared_ptr<SpecialNamesInterface>, SpecialNamesInterfaceTrampoline>(module, "SpecialNamesInterface")
        .def(py::init<>())
        .def("dispatch", [](SpecialNamesInterface& self, const ::smoke::SpecialNamesInterface::Callback& callback) {
            return self.dispatch(callback);
        }, py::arg("callback"))
        ;
}

