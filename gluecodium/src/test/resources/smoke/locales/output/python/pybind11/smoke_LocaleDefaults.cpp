

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
#include "gluecodium/Locale.h"
#include "smoke/LocaleDefaults.h"

using LocaleDefaults = ::smoke::LocaleDefaults;



void register_smoke_LocaleDefaults(py::module_& module) {
auto cls_LocaleDefaults = py::class_<LocaleDefaults>(module, "smoke_LocaleDefaults")
        .def_property("english", [](const LocaleDefaults& self) -> decltype(auto) {
            return
                (self.english)
            ;
        }, [](LocaleDefaults& self, const ::gluecodium::Locale& value) {

                self.english = value;

        })
        .def_property("lat_am_spanish", [](const LocaleDefaults& self) -> decltype(auto) {
            return
                (self.lat_am_spanish)
            ;
        }, [](LocaleDefaults& self, const ::gluecodium::Locale& value) {

                self.lat_am_spanish = value;

        })
        .def_property("romansh_sursilvan", [](const LocaleDefaults& self) -> decltype(auto) {
            return
                (self.romansh_sursilvan)
            ;
        }, [](LocaleDefaults& self, const ::gluecodium::Locale& value) {

                self.romansh_sursilvan = value;

        })
        .def_property("serbian_cyrillic", [](const LocaleDefaults& self) -> decltype(auto) {
            return
                (self.serbian_cyrillic)
            ;
        }, [](LocaleDefaults& self, const ::gluecodium::Locale& value) {

                self.serbian_cyrillic = value;

        })
        .def_property("traditional_chinese_taiwan", [](const LocaleDefaults& self) -> decltype(auto) {
            return
                (self.traditional_chinese_taiwan)
            ;
        }, [](LocaleDefaults& self, const ::gluecodium::Locale& value) {

                self.traditional_chinese_taiwan = value;

        })
        .def_property("zuerich_german", [](const LocaleDefaults& self) -> decltype(auto) {
            return
                (self.zuerich_german)
            ;
        }, [](LocaleDefaults& self, const ::gluecodium::Locale& value) {

                self.zuerich_german = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::Locale, ::gluecodium::Locale, ::gluecodium::Locale, ::gluecodium::Locale, ::gluecodium::Locale, ::gluecodium::Locale>(), py::arg("english"), py::arg("lat_am_spanish"), py::arg("romansh_sursilvan"), py::arg("serbian_cyrillic"), py::arg("traditional_chinese_taiwan"), py::arg("zuerich_german"))
        ;


}
