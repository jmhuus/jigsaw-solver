import { Directive } from '@angular/core';
import { HostListener } from '@angular/core';

@Directive({
  selector: '[appDnd]'
})
export class DndDirective {
  fileOver: any;

  constructor() { }

  @HostListener('dragover', ['$event'])
  onDragOver(evt) {
    evt.preventDefault();
    evt.stopPropagation();

    console.log('Drag Over');
  }

  @HostListener('dragleave', ['$event'])
  onDragLeave(evt) {
    evt.preventDefault();
    evt.stopPropagation();

    console.log('Drag Leave');
  }

  @HostListener('drop', ['$event'])
  onDrop(evt) {
    evt.preventDefault();
    evt.stopPropagation();

    console.log('Drop');

    // Retrieve dropped file
    this.fileOver = false;
    let files = evt.dataTransfer.files;
    if (files.length > 0) {
      console.log('You dropped ${files.length} files.');
    }
  }
  
}
