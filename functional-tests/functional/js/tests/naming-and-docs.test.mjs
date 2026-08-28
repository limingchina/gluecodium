import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { loadPackage } from './load-package.mjs';

const packageRoot = new URL('../../js/', import.meta.url);
const commentsDeclaration = new URL('test/Comments.d.ts', packageRoot);
const commentsLinksDeclaration = new URL('test/CommentsLinks.d.ts', packageRoot);
const multilineCommentsDeclaration = new URL('test/MultiLineComments.d.ts', packageRoot);
const platformNamesDeclaration = new URL('test/PlatformNames.d.ts', packageRoot);
const keywordClassDeclaration = new URL('smoke/Class.d.ts', packageRoot);
const keywordTypesDeclaration = new URL('smoke/Types.d.ts', packageRoot);

test('generated declarations preserve comments and links as JSDoc', async () => {
    const declaration = await readFile(commentsDeclaration, 'utf8');

    assert.match(declaration, /\* This is some very useful \./);
    assert.match(declaration, /\* @param input Very useful input parameter/);
    assert.match(declaration, /\* @returns Usefulness of the input/);

    const multilineDeclaration = await readFile(multilineCommentsDeclaration, 'utf8');
    assert.match(multilineDeclaration, /\* asterisk/);
    assert.match(multilineDeclaration, /\* needs/);
    assert.match(multilineDeclaration, /\* escaping/);

    const linksDeclaration = await readFile(commentsLinksDeclaration, 'utf8');
    assert.match(linksDeclaration, /`Comments\.SomeCommentedEnum`/);
    assert.match(linksDeclaration, /`CommentsLinks\.randomMethod\.inputParameter`/);
});

test('JavaScript platform names are public declaration and runtime names', async () => {
    const declaration = await readFile(platformNamesDeclaration, 'utf8');
    assert.match(declaration, /export interface PlatformNames/);

    const platformTypes = await loadPackage('test');
    assert.equal(typeof platformTypes.PlatformNames, 'object');
    assert.equal(typeof platformTypes.BasicStruct, 'object');
    assert.equal(typeof platformTypes.BasicEnum, 'function');
    assert.equal(typeof platformTypes.PlatformNamesInterface, 'function');
    assert.equal(typeof platformTypes.PlatformNamesListener, 'function');
});

test('keyword names remain valid public TypeScript identifiers', async () => {
    const classDeclaration = await readFile(keywordClassDeclaration, 'utf8');
    assert.match(classDeclaration, /export class Class/);
    assert.match(classDeclaration, /fun\(/);
    assert.match(classDeclaration, /property:/);

    const typesDeclaration = await readFile(keywordTypesDeclaration, 'utf8');
    assert.match(typesDeclaration, /export interface Types/);

    const keywordTypes = await loadPackage('smoke');
    assert.equal(typeof keywordTypes.Types, 'object');
    assert.equal(typeof keywordTypes.Class, 'function');
    assert.equal(typeof keywordTypes.Enum, 'function');
    assert.equal(typeof keywordTypes.Struct, 'object');
});