

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentInterfaceWithIncludes.h"
#include "smoke/ShouldNotInclude.h"
#include "functional"
#include "memory"

void register_ParentInterfaceWithIncludes(py::module_& module) {
    py::class_<ParentInterfaceWithIncludes, std::shared_ptr<ParentInterfaceWithIncludes>>(module, "ParentInterfaceWithIncludes")
        .def("root_method", &ParentInterfaceWithIncludes::root_method, py::arg("input1"), py::arg("input2"))
        .def("not_in_java", &ParentInterfaceWithIncludes::not_in_java)
        .def_property("root_property", &ParentInterfaceWithIncludes::get_root_property)
        .def_property("not_in_java_property", &ParentInterfaceWithIncludes::get_not_in_java_property)
        ;
}

