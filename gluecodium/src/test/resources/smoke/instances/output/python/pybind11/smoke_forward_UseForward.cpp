

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SimpleClass.h"
#include "smoke/SimpleInterface.h"
#include "smoke/forward/Class1.h"
#include "smoke/forward/Class2.h"
#include "smoke/forward/UseForward.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseForward = ::smoke::forward::UseForward;

class UseForwardTrampoline : public UseForward {
public:
    using UseForward::UseForward;

    void use_it(
            const ::std::shared_ptr< ::smoke::forward::Class1 >& param1, const ::std::shared_ptr< ::smoke::forward::Class2 >& param2, const ::std::shared_ptr< ::smoke::SimpleClass >& simple_class, const ::std::shared_ptr< ::smoke::SimpleInterface >& simple_interface ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, UseForward, use_it, param1, param2, simple_class, simple_interface);
    }
};

void register_UseForward(py::module_& module) {
    py::class_<UseForward, std::shared_ptr<UseForward>, UseForwardTrampoline>(module, "UseForward")
        .def(py::init<>())
        .def("use_it", [](UseForward& self, const ::std::shared_ptr< ::smoke::forward::Class1 >& param1, const ::std::shared_ptr< ::smoke::forward::Class2 >& param2, const ::std::shared_ptr< ::smoke::SimpleClass >& simple_class, const ::std::shared_ptr< ::smoke::SimpleInterface >& simple_interface) {
            return self.use_it(param1, param2, simple_class, simple_interface);
        }, py::arg("param1"), py::arg("param2"), py::arg("simple_class"), py::arg("simple_interface"))
        ;
}

