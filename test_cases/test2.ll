; ModuleID = './test2.ll'
source_filename = "test2.c"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128"
target triple = "arm64-apple-macosx15.0.0"

; Function Attrs: noinline nounwind ssp uwtable(sync)
define i32 @main() #0 !dbg !9 {
entry:
  %call = call i32 @rand(i32 noundef 0, i32 noundef 20), !dbg !14
  call void @llvm.dbg.value(metadata i32 %call, metadata !15, metadata !DIExpression()), !dbg !16
  call void @llvm.dbg.value(metadata i32 0, metadata !17, metadata !DIExpression()), !dbg !16
  %cmp = icmp slt i32 %call, 5, !dbg !18
  br i1 %cmp, label %land.lhs.true, label %if.end, !dbg !20

land.lhs.true:                                    ; preds = %entry
  %cmp1 = icmp sgt i32 %call, 10, !dbg !21
  br i1 %cmp1, label %if.then, label %if.end, !dbg !22

if.then:                                          ; preds = %land.lhs.true
  call void @llvm.dbg.value(metadata i32 8, metadata !17, metadata !DIExpression()), !dbg !16
  br label %if.end, !dbg !23

if.end:                                           ; preds = %if.then, %land.lhs.true, %entry
  %b.0 = phi i32 [ 8, %if.then ], [ 0, %land.lhs.true ], [ 0, %entry ], !dbg !16
  call void @llvm.dbg.value(metadata i32 %b.0, metadata !17, metadata !DIExpression()), !dbg !16
  %cmp2 = icmp eq i32 %b.0, 8, !dbg !25
  call void @svf_assert(i1 noundef zeroext %cmp2), !dbg !26
  ret i32 0, !dbg !27
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

declare i32 @rand(i32 noundef, i32 noundef) #2

declare void @svf_assert(i1 noundef zeroext) #2

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare void @llvm.dbg.value(metadata, metadata, metadata) #1

attributes #0 = { noinline nounwind ssp uwtable(sync) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+crypto,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+sm4,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #1 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #2 = { "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+crypto,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+sm4,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6, !7}
!llvm.ident = !{!8}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "Homebrew clang version 16.0.6", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, splitDebugInlining: false, nameTableKind: None, sysroot: "/Library/Developer/CommandLineTools/SDKs/MacOSX14.sdk", sdk: "MacOSX14.sdk")
!1 = !DIFile(filename: "test2.c", directory: "/Users/z5489735/2023/0424/Software-Security-Analysis-Marker/solution/SVF-Under/test_cases")
!2 = !{i32 7, !"Dwarf Version", i32 4}
!3 = !{i32 2, !"Debug Info Version", i32 3}
!4 = !{i32 1, !"wchar_size", i32 4}
!5 = !{i32 8, !"PIC Level", i32 2}
!6 = !{i32 7, !"uwtable", i32 1}
!7 = !{i32 7, !"frame-pointer", i32 1}
!8 = !{!"Homebrew clang version 16.0.6"}
!9 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 5, type: !10, scopeLine: 5, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !13)
!10 = !DISubroutineType(types: !11)
!11 = !{!12}
!12 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!13 = !{}
!14 = !DILocation(line: 6, column: 13, scope: !9)
!15 = !DILocalVariable(name: "a", scope: !9, file: !1, line: 6, type: !12)
!16 = !DILocation(line: 0, scope: !9)
!17 = !DILocalVariable(name: "b", scope: !9, file: !1, line: 7, type: !12)
!18 = !DILocation(line: 8, column: 11, scope: !19)
!19 = distinct !DILexicalBlock(scope: !9, file: !1, line: 8, column: 9)
!20 = !DILocation(line: 8, column: 15, scope: !19)
!21 = !DILocation(line: 8, column: 20, scope: !19)
!22 = !DILocation(line: 8, column: 9, scope: !9)
!23 = !DILocation(line: 10, column: 5, scope: !24)
!24 = distinct !DILexicalBlock(scope: !19, file: !1, line: 8, column: 26)
!25 = !DILocation(line: 11, column: 18, scope: !9)
!26 = !DILocation(line: 11, column: 5, scope: !9)
!27 = !DILocation(line: 12, column: 5, scope: !9)
