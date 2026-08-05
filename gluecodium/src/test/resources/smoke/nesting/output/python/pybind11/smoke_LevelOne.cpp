

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
#include "smoke/LevelOne.h"
#include "smoke/OuterClass.h"
#include "smoke/OuterInterface.h"
#include "memory"
#include "string"

using LevelOne = ::smoke::LevelOne;
using LevelTwo = ::smoke::LevelOne::LevelTwo;
using LevelThree = ::smoke::LevelOne::LevelTwo::LevelThree;
using LevelFour = ::smoke::LevelOne::LevelTwo::LevelThree::LevelFour;
using LevelFourEnum = ::smoke::LevelOne::LevelTwo::LevelThree::LevelFourEnum;



void register_smoke_LevelOne(py::module_& module) {
auto cls_LevelOne = py::class_<LevelOne, std::shared_ptr<LevelOne>>(module, "smoke_LevelOne")
        .def("__gluecodium_id__", [](const LevelOne& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_LevelOneLevelTwo = py::class_<LevelTwo, std::shared_ptr<LevelTwo>>(cls_LevelOne, "LevelTwo")
        .def("__gluecodium_id__", [](const LevelTwo& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_LevelOneLevelTwoLevelThree = py::class_<LevelThree, std::shared_ptr<LevelThree>>(cls_LevelOneLevelTwo, "LevelThree")
        .def("__gluecodium_id__", [](const LevelThree& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("foo", &LevelThree::foo, py::arg("input"))
        ;

auto cls_LevelOneLevelTwoLevelThreeLevelFour = py::class_<LevelFour>(cls_LevelOneLevelTwoLevelThree, "LevelFour")
        .def_readwrite("string_field", &LevelFour::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        .def_static("foo_factory", &LevelFour::foo_factory)
        ;

auto cls_LevelOneLevelTwoLevelThreeLevelFourEnum = py::enum_<LevelFourEnum>(cls_LevelOneLevelTwoLevelThree, "LevelFourEnum")
        .value("NONE", LevelFourEnum::NONE)
        ;


}
