# Copyright (C) 2016-2026 HERE Europe B.V.
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
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""Locale type mapping tests for the Python (pybind11) bindings.

Locale is mapped to a plain Python ``str`` containing the BCP 47 language tag
(e.g. ``"en-US"``, ``"sr-Cyrl"``). This mirrors the approach used by the Dart
and Swift generators, where the BCP 47 language tag takes precedence on
conversion from C++ to the platform type.
"""

import functional
from test.Locales import Locales
from test.LocaleDefaults import LocaleDefaults
from test.LocaleGenerics import LocaleGenerics
from test.LocalesStruct import LocalesStruct

import pytest


class TestLocales:
    def test_locale_round_trip(self):
        result = Locales.locale_round_trip("en-US")

        assert result == "en-US"

    def test_locale_round_trip_simple(self):
        result = Locales.locale_round_trip("en")

        assert result == "en"

    def test_locale_round_trip_with_script(self):
        result = Locales.locale_round_trip("sr-Cyrl")

        assert result == "sr-Cyrl"

    def test_locale_round_trip_strip_tag(self):
        # localeRoundTripStripTag strips the BCP 47 language tag and returns
        # only the ISO code components. Since Python passes Locale as a plain
        # BCP 47 tag string (setting only the language_tag field in C++), the
        # ISO code fields are empty after stripping. The result is "und"
        # (undefined locale) per BCP 47.
        result = Locales.locale_round_trip_strip_tag("en-US")

        assert result == "und"

    def test_locale_round_trip_nullable(self):
        result = Locales.locale_round_trip_nullable("en-US")

        assert result == "en-US"

    def test_locale_round_trip_nullable_null(self):
        result = Locales.locale_round_trip_nullable(None)

        assert result is None

    def test_locale_property_round_trip(self):
        Locales.locale_property_set("fr-CA")

        result = Locales.locale_property()
        assert result == "fr-CA"

    def test_locale_with_malformed_tag(self):
        # localeWithMalformedTag returns a Locale created from a malformed
        # language tag string "@#$%". Since language_tag is set, the caster
        # returns it as-is.
        result = Locales.locale_with_malformed_tag()

        assert result == "@#$%"

    def test_locale_with_malformed_language(self):
        # localeWithMalformedLanguage returns Locale("@#$%", "bar", "baz"),
        # setting language_code="@#$%", country_code="bar", script_code="baz".
        # No language_tag, so the caster synthesizes: language-script-country.
        result = Locales.locale_with_malformed_language()

        assert result == "@#$%-baz-bar"

    def test_locale_with_malformed_country(self):
        # localeWithMalformedCountry returns Locale("foo", "@#$%", "baz"),
        # setting language_code="foo", country_code="@#$%", script_code="baz".
        # No language_tag, so the caster synthesizes: language-script-country.
        result = Locales.locale_with_malformed_country()

        assert result == "foo-baz-@#$%"

    def test_locale_with_malformed_script(self):
        # localeWithMalformedScript returns Locale("foo", "bar", "@#$%"),
        # setting language_code="foo", country_code="bar", script_code="@#$%".
        # No language_tag, so the caster synthesizes: language-script-country.
        result = Locales.locale_with_malformed_script()

        assert result == "foo-@#$%-bar"


class TestLocalesStruct:
    def test_locales_struct_round_trip(self):
        input_struct = LocalesStruct("en-US", "fr-CA")

        result = LocalesStruct.locales_struct_round_trip(input_struct)

        assert result.primary_locale == "en-US"
        assert result.secondary_locale == "fr-CA"

    def test_locales_struct_round_trip_null_secondary(self):
        input_struct = LocalesStruct("en-US", None)

        result = LocalesStruct.locales_struct_round_trip(input_struct)

        assert result.primary_locale == "en-US"
        assert result.secondary_locale is None

    def test_locales_struct_equality(self):
        a = LocalesStruct("en-US", "fr-CA")
        b = LocalesStruct("en-US", "fr-CA")

        assert a == b

    def test_locales_struct_inequality(self):
        a = LocalesStruct("en-US", "fr-CA")
        b = LocalesStruct("en-US", "de-DE")

        assert a != b


class TestLocaleDefaults:
    def test_locale_defaults_english(self):
        defaults = LocaleDefaults()

        assert defaults.english == "en"

    def test_locale_defaults_lat_am_spanish(self):
        defaults = LocaleDefaults()

        assert defaults.lat_am_spanish == "es-419"

    def test_locale_defaults_serbian_cyrillic(self):
        defaults = LocaleDefaults()

        assert defaults.serbian_cyrillic == "sr-Cyrl"

    def test_locale_defaults_traditional_chinese_taiwan(self):
        defaults = LocaleDefaults()

        assert defaults.traditional_chinese_taiwan == "nan-Hant-TW"

    def test_locale_defaults_from_cpp(self):
        defaults = LocaleDefaults.get_cpp_defaults()

        assert defaults.english == "en"
        assert defaults.lat_am_spanish == "es-419"
        assert defaults.serbian_cyrillic == "sr-Cyrl"
        assert defaults.traditional_chinese_taiwan == "nan-Hant-TW"


class TestLocaleGenerics:
    def test_locale_list_round_trip(self):
        input_list = ["en-US", "fr-CA", "sr-Cyrl"]

        result = LocaleGenerics.locale_list_round_trip(input_list)

        assert result == input_list

    def test_locale_set_round_trip(self):
        input_set = {"en-US", "fr-CA", "sr-Cyrl"}

        result = LocaleGenerics.locale_set_round_trip(input_set)

        assert result == input_set

    def test_locale_keys_map_round_trip(self):
        input_map = {"en-US": "English", "fr-CA": "French"}

        result = LocaleGenerics.locale_keys_map_round_trip(input_map)

        assert result == input_map

    def test_locale_values_map_round_trip(self):
        input_map = {"greeting": "en-US", "farewell": "fr-CA"}

        result = LocaleGenerics.locale_values_map_round_trip(input_map)

        assert result == input_map
