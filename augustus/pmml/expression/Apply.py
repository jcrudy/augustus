#!/usr/bin/env python

# Copyright (C) 2006-2013  Open Data ("Open Data" refers to
# one or more of the following companies: Open Data Partners LLC,
# Open Data Research LLC, or Open Data Capital LLC.)
#
# This file is part of Augustus.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module defines the Apply class."""

from augustus.core.defs import defs
from augustus.core.PmmlExpression import PmmlExpression
from augustus.core.DataColumn import DataColumn
from augustus.core.FieldCastMethods import FieldCastMethods

class Apply(PmmlExpression):
    """Apply implements an expression that applies a predefined
    function on a set of input arguments.

    U{PMML specification<http://www.dmg.org/v4-1/Transformations.html>}.
    """
    def evaluate(self, dataTable, functionTable, performanceTable):
        """Evaluate the expression, using a DataTable as input.

        @type dataTable: DataTable
        @param dataTable: The input DataTable, containing any fields that might be used to evaluate this expression.
        @type functionTable: FunctionTable
        @param functionTable: The FunctionTable, containing any functions that might be called in this expression.
        @type performanceTable: PerformanceTable
        @param performanceTable: A PerformanceTable for measuring the efficiency of the calculation.
        @rtype: DataColumn
        @return: The result of the calculation as a DataColumn.
        """

        performanceTable.begin("Apply")
        
        function = functionTable.get(self.get("function"))
        if function is None:
            raise LookupError("Apply references function \"%s\", but it does not exist" % self.get("function"))

        arguments = self.childrenOfClass(PmmlExpression)

        performanceTable.pause("Apply")
        dataColumn = function.evaluate(dataTable, functionTable, performanceTable, arguments)
        performanceTable.unpause("Apply")

        mask = FieldCastMethods.applyInvalidValueTreatment(dataColumn.mask, self.get("invalidValueTreatment"))
        data, mask = FieldCastMethods.applyMapMissingTo(dataColumn.fieldType, dataColumn.data, mask, self.get("mapMissingTo"))

        performanceTable.end("Apply")
        return DataColumn(dataColumn.fieldType, data, mask)
