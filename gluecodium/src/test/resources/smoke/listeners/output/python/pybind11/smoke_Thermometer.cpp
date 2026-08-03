

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
#include "gluecodium/DurationHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/TemperatureObserver.h"
#include "smoke/Thermometer.h"
#include "chrono"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

using Thermometer = ::smoke::Thermometer;
using SomeThermometerErrorCode = ::smoke::Thermometer::SomeThermometerErrorCode;



void register_smoke_Thermometer(py::module_& module) {
auto cls_Thermometer = py::class_<Thermometer, std::shared_ptr<Thermometer>>(module, "smoke_Thermometer")
        .def("__gluecodium_id__", [](const Thermometer& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("make_with_duration", [](const ::std::chrono::seconds interval, const ::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >& observers) {
                return Thermometer::make_with_duration(interval, observers);
            }, py::arg("interval"), py::arg("observers"))
        .def_static("make_without_duration", [](const ::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >& observers) {
                return Thermometer::make_without_duration(observers);
            }, py::arg("observers"))
        .def_static("throwing_make", [](const int32_t id, const ::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >& observers) {
                return Thermometer::throwing_make(id, observers);
            }, py::arg("id"), py::arg("observers"))
        .def_static("nothrow_make", [](const ::std::string& label, const ::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >& nice_observers) {
                return Thermometer::nothrow_make(label, nice_observers);
            }, py::arg("label"), py::arg("nice_observers"))
        .def_static("another_throwing_make", [](const bool dummy, const ::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >& observers) {
                return Thermometer::another_throwing_make(dummy, observers);
            }, py::arg("dummy"), py::arg("observers"))
                .def_static("notify_observers", [](const ::std::shared_ptr< ::smoke::Thermometer >& thermometer, const ::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >& some_observers) {
                        Thermometer::notify_observers(thermometer, some_observers);
                }, py::arg("thermometer"), py::arg("some_observers"))
                .def_static("throwing_notify_observers", [](const ::std::shared_ptr< ::smoke::Thermometer >& thermometer, const ::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >& some_observers) {
                        return Thermometer::throwing_notify_observers(thermometer, some_observers);
                }, py::arg("thermometer"), py::arg("some_observers"))
        .def("force_update", &Thermometer::force_update)
        .def("get_celsius", &Thermometer::get_celsius)
        .def("get_kelvin", &Thermometer::get_kelvin)
        .def("get_fahrenheit", &Thermometer::get_fahrenheit)
        ;

auto cls_ThermometerSomeThermometerErrorCode = py::enum_<SomeThermometerErrorCode>(cls_Thermometer, "SomeThermometerErrorCode")
        .value("ERROR_NONE", SomeThermometerErrorCode::ERROR_NONE)
        .value("ERROR_FATAL", SomeThermometerErrorCode::ERROR_FATAL)
        ;

    static py::object py_exc =
        py::module_::import("smoke.Thermometer").attr("Thermometer").attr("NotificationError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::string& e) {
            const auto message = pybind11::detail::ReturnErrorToString<::std::string>::convert(e);
            PyErr_SetString(py_exc.ptr(), message.c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::string>(py_exc.ptr());

    static py::exception<::std::error_code> exc(cls_Thermometer, "AnotherNotificationError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc.ptr());


}
