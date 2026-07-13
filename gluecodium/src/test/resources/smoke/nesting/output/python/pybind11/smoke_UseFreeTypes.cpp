

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Free.h"
#include "smoke/FreeEnum.h"
#include "smoke/FreePoint.h"
#include "smoke/FreeTypeDef.h"
#include "smoke/UseFreeTypes.h"

void register_UseFreeTypes(py::module_& module) {
    py::class_<UseFreeTypes>(module, "UseFreeTypes")
        .def("do_stuff", &UseFreeTypes::do_stuff, py::arg("point"), py::arg("mode"))
        ;
}

