

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CommentsMarkdown.h"

using CommentsMarkdown = ::smoke::CommentsMarkdown;



void register_smoke_CommentsMarkdown(py::module_& module) {
auto cls_CommentsMarkdown = py::class_<CommentsMarkdown, std::shared_ptr<CommentsMarkdown>>(module, "smoke_CommentsMarkdown")
        .def("__gluecodium_id__", [](const CommentsMarkdown& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
