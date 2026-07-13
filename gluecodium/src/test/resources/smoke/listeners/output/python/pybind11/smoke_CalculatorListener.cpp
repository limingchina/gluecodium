

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/CalculatorListener.h"
#include "memory"
#include "vector"

void register_CalculatorListener(py::module_& module) {
    py::class_<CalculatorListener, std::shared_ptr<CalculatorListener>>(module, "CalculatorListener")
        .def("on_calculation_result", &CalculatorListener::on_calculation_result, py::arg("calculation_result"))
        .def("on_calculation_result_const", &CalculatorListener::on_calculation_result_const, py::arg("calculation_result"))
        .def("on_calculation_result_struct", &CalculatorListener::on_calculation_result_struct, py::arg("calculation_result"))
        .def("on_calculation_result_array", &CalculatorListener::on_calculation_result_array, py::arg("calculation_result"))
        .def("on_calculation_result_map", &CalculatorListener::on_calculation_result_map, py::arg("calculation_results"))
        .def("on_calculation_result_instance", &CalculatorListener::on_calculation_result_instance, py::arg("calculation_result"))
        ;
}

