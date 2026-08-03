

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PlatformComments.h"
#include "string"

using PlatformComments = ::smoke::PlatformComments;
using Something = ::smoke::PlatformComments::Something;
using SomeEnum = ::smoke::PlatformComments::SomeEnum;



void register_smoke_PlatformComments(py::module_& module) {
auto cls_PlatformComments = py::class_<PlatformComments, std::shared_ptr<PlatformComments>>(module, "smoke_PlatformComments")
        .def("__gluecodium_id__", [](const PlatformComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("do_nothing", &PlatformComments::do_nothing)
        .def("do_magic", &PlatformComments::do_magic)
        .def("some_method_with_all_comments", &PlatformComments::some_method_with_all_comments, py::arg("input"))
        .def("some_deprecated_method", &PlatformComments::some_deprecated_method)
        ;

auto cls_PlatformCommentssomething = py::class_<Something>(cls_PlatformComments, "Something")
        .def_readwrite("nothing", &Something::nothing)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("nothing"))
        ;

auto cls_PlatformCommentsSomeEnum = py::enum_<SomeEnum>(cls_PlatformComments, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        .value("USEFUL", SomeEnum::USEFUL)
        ;

    static py::exception<::std::error_code> exc(cls_PlatformComments, "SomethingWrongError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc.ptr());


}
